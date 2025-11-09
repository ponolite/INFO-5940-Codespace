# app.py
"""
Multi-Agent Travel Planner

Highlights:
- Clear separation of concerns (tools, agents, orchestration, UI)
- Simple global logger to display tool calls live in the sidebar
- Planner → Reviewer pipeline enforced before rendering any answer
- Minimal dependencies and straightforward control flow
"""

from __future__ import annotations

import os
import asyncio
import time
from typing import Callable, Dict, List, Optional, Any

import streamlit as st
from dotenv import load_dotenv
from tavily import TavilyClient

# ──────────────────────────────────────────────────────────────────────────────
# Environment & Globals
# ──────────────────────────────────────────────────────────────────────────────

load_dotenv()  # Loads variables from a local .env if present
os.environ.setdefault("OPENAI_LOG", "error")
os.environ.setdefault("OPENAI_TRACING", "false")

# Tool call logger: the UI sets this per request. The tool checks it and logs.
# Using a simple global makes this easy to teach and reason about.
TOOL_LOGGER: Optional[Callable[[Dict[str, Any]], None]] = None


def set_tool_logger(logger: Optional[Callable[[Dict[str, Any]], None]]) -> None:
    """Install or remove the UI logger used by tools to report activity."""
    global TOOL_LOGGER
    TOOL_LOGGER = logger


def log_tool_event(event: Dict[str, Any]) -> None:
    """If a logger is installed, send the event to the UI."""
    if TOOL_LOGGER is not None:
        try:
            TOOL_LOGGER(event)
        except Exception:
            # Logging should never break the app or the tool itself
            pass


def redact_for_logs(value: Any) -> Any:
    """
    Make sure we don't leak secrets and keep logs small.
    This is deliberately simple for teaching.
    """
    if isinstance(value, str):
        low = value.lower()
        if any(k in low for k in ("api_key", "token", "secret", "password")):
            return "[redacted]"
        return value if len(value) <= 300 else value[:120] + "… [truncated]"
    if isinstance(value, dict):
        return {k: ("[redacted]" if any(s in k.lower() for s in ("key", "token", "secret", "password"))
                    else redact_for_logs(v))
                for k, v in value.items()}
    if isinstance(value, list):
        return [redact_for_logs(v) for v in value]
    return value


# ──────────────────────────────────────────────────────────────────────────────
# Agent Framework Imports (provided by you)
# ──────────────────────────────────────────────────────────────────────────────
# These come from your own framework. We assume:
# - Agent: defines a model + instructions + optional tools
# - Runner.run(agent, input): executes an agent and returns an object with text
from agents import Agent, Runner, function_tool  # type: ignore


# ──────────────────────────────────────────────────────────────────────────────
# Tools
# ──────────────────────────────────────────────────────────────────────────────

@function_tool
def internet_search(query: str) -> str:
    """
    Internet search backed by Tavily.
    - Reads TAVILY_API_KEY from environment.
    - Sends simple log events before/after the call so the UI can show activity.
    """
    log_tool_event({"type": "call", "tool": "internet_search", "args": {"query": redact_for_logs(query)}})

    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            msg = "missing TAVILY_API_KEY in environment."
            log_tool_event({"type": "error", "tool": "internet_search", "error": msg})
            return f"Search error: {msg}"

        client = TavilyClient(api_key=api_key)
        response = client.search(query, max_results=3)

        items = response.get("results", [])
        lines = [f"- {it.get('title', 'N/A')}: {it.get('content', 'N/A')}" for it in items]
        output = "\n".join(lines) if lines else "No results found."

        log_tool_event({
            "type": "result",
            "tool": "internet_search",
            "preview": redact_for_logs(output[:400] + ("…" if len(output) > 400 else "")),
        })
        return output

    except Exception as e:
        log_tool_event({"type": "error", "tool": "internet_search", "error": str(e)})
        return f"Search error: {e}"

    finally:
        log_tool_event({"type": "end", "tool": "internet_search"})


# ──────────────────────────────────────────────────────────────────────────────
# Agents
# ──────────────────────────────────────────────────────────────────────────────

# BEGIN SOLUTION

REVIEWER_INSTRUCTIONS = """
You are the **Reviewer Agent** colloborating in a travel-planning pipeline with another agent called **Planner Agent**.

You'll receive the original user prompt, which is implicit in the planner's text. You'll also receive a draft itinerary produced by the Planner Agent.

Your goals are:
1. Check the draft for factual feasibility and trip logic (e.g., opening hours, ticket prices/availability...).
2. Point out any unrealistic or conflicting activities.
3. Use the provided `internet_search` tool whenever you need to carry out real-time fact-checking (e.g., validate opening days/hours, ticket prices/availability, or inter-city transport feasibility...).
4. Generate a concrete "Delta List" (a list that specifies the concrete changes and reasons why).
5. Then output a revised "Finalized Itinerary" that apply those changes.
6. Maintain a clear and well-organized user-facing tone.

Important operating rules:
- You **can** and **should** call the `internet_search(query: str)` tool to fact-check every time you've ofund something illogical or infeasible.
- You MUST make at least one call to `internet_search(query: str)` for every itinerary you review, even if the plan looks reasonable, so the system can log tool activity. Prioritize checking a time-sensitive or high-profile attraction from the plan (e.g. museums, observatories, national parks, ferries).
- If you find something obviously impractical (e.g., an attraction that closes early, too many activities too far apart...), then search for it and fix it.
- If there is something unverifiable (no result found, unknown attraction), you can retain that information but you have to mark it as “verify locally before visiting."

You need to check for:
1. **Time feasibility**: verify if opening hours are compatible with the planner’s time blocks (morning/afternoon/evening)? If not, recommend a time change or another attraction in the same city.
2. **Geographic/logistics feasibility**: if the day switches between far-apart cities or neighborhoods impractically, try to group activities by one area and suggest cutting 1 item (to remove outlier from the schedule).
3. **Budget adherence**: if the planner implies a strict budget even though that day's schedule clearly exceeds the budget, pay attention to that and suggest a lower-cost alternative. 
4. **Pacing**: if a day has too many items (e.g., 5–6 major items), note that as being too dense of a schedule and propose  it as too dense and propose removing dense activities and/or add leisure time.
5. **Clarity**: if the planner hasn't clearly mentioned locations, desitnations or transit in the schedule, add them. 

Your output MUST follow this structure:

1. **Delta List**  
   - [Day X, Item] Title of the change made — Reason (include any available information from searches if applicable)  
   - …  
   If no issues were found, write: “- No issues found.”

2. **Final Itinerary (Revised)**  
   - Maintain the structural integrity and the day-by-day order as the planner's, but apply your changes - or your deltas - to the final itinerary.
   - For each day, insert: day title, city/area, activities with time details, and (if the planner had them) estimated costs/logistics.
   - Try to be concise but complete enough, so that a traveler can easily follow what you mean.

Notes on style:
- Don't get rid of good content from the planner unless you can replace it with something equivalent or feasible. 
- Don't say you can't verify anything especially when you haven't tried to search the internet first for time-critical items. 
- Do NOT invent new tools or APIs — only use `internet_search`.
- Write in markdown so Streamlit can render it nicely.
"""

PLANNER_INSTRUCTIONS = """
You are the **Planner Agent** colloborating in a travel-planning app with with another agent called **Reviewer Agent**.

Your role: assess a vague travel prompt from a user (e.g. "Plan a week-long Europe trip for a student on a $1,500 budget who loves history and food.") and specify it into a **clear, structured, day-by-day travel itinerary.**

Constraints and expected behavior:
- You don't have internet access. Thus, you must plan from general travel knowledge and reasonable assumptions.
- You absolutely have to abide by user constraints: duration, budget (be as realistic as you can), interests (history, food) andd pacing (don’t try to over-schedule or add too many activities to a day).
- You must organize nearby activities together to lessen travel duration. 
- You must have enough detail in your itinerary for the Reviewer Agent to verify, review and validate it later. 
- Be specific about the location of any places you recommended and provide at least 2 alternatives, e.g., must be clearer than something vague like "grab dinner at a food market" (specify which food market or places close to the attraction).

Your itinerary MUST include:
1. **Schedule Summary** (1 short paragraph): cities/areas visited, overall emotional vibe, key assumptions (e.g. “uses public transit”).
2. **Budget Assumptions**: daily amount (accommodation, food, activities, transport). Keep numbers approximate but realistic.
3. **Day-by-Day Itinerary**:
   For EACH day:
   - **Day No. and City/Area**
   - Morning: time interval and time duration, activity, location/neighborhood, most optimal way to get there, short description
   - Afternoon: time interval and time duration, activity, location/neighborhood, most optimal way to get there, short description
   - Evening: time interval and time duration, activity, location/neighborhood, most optimal way to get there, short description
   - Logistics: how to travel between the mentioned main items (e.g., is it walk/metro/train or others)
   - Estimated daily budget (rough)
   - Notes (tickets recommended, alternative if weather is bad, etc.)

Planning guidance:
- If the trip is carried out between various cities, organize days by city (e.g. Days 1–3 Paris).
- If the budget is limited, try to prioritize free/low-cost items. 
- If the user specifies concrete interests, be certain to include that interest in at least half of the days in the itinerary.
- If the user is a solo traveler, try to incorporate social/flexible evening schedule since they have more opportunties to explore further.
- If dates aren’t provided, assume typical opening schedule but flag items that may necessitate advance booking.

Output outline (in markdown):
- Begin with `## Trip Summary`
- Then `## Budget Assumptions`
- Then `## Day-by-Day Itinerary`
- Under Day-by-Day, use `### Day 1 …`, `### Day 2 …`, etc.
- Keep language concise, clear and friendly, as this will be shown to the user.

Important to note: you are only PLANNING. The Reviewer will fact-check and adjust later.
"""

reviewer_agent = Agent(
    name="Reviewer Agent",
    model="openai.gpt-4o",
    instructions=REVIEWER_INSTRUCTIONS.strip(),
    tools=[internet_search], # Add the internet_search tool to the reviewer_agent.
)

planner_agent = Agent(
    name="Planner Agent",
    model="openai.gpt-4o",
    instructions=PLANNER_INSTRUCTIONS.strip(),
)

# END SOLUTION


# ──────────────────────────────────────────────────────────────────────────────
# Orchestration Helpers
# ──────────────────────────────────────────────────────────────────────────────

def extract_text(result_obj: Any) -> str:
    """
    Pull a usable string from the Runner result in a tolerant way.
    Your Runner may expose final_output, text, or __str__.
    """
    return (
        getattr(result_obj, "final_output", None)
        or getattr(result_obj, "text", None)
        or str(result_obj)
    )


def run_planner(user_text: str) -> str:
    """Run the Planner and return its itinerary text."""
    result = asyncio.run(Runner.run(planner_agent, user_text))
    return extract_text(result)


def run_reviewer(plan_text: str) -> str:
    """Run the Reviewer on the planner’s output and return validated text."""
    result = asyncio.run(Runner.run(reviewer_agent, plan_text))
    return extract_text(result)


# ──────────────────────────────────────────────────────────────────────────────
# Streamlit UI
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Travel Planner", page_icon="✈️")

st.title("✈️ Multi-Agent Travel Planner")
st.caption("Planner → Reviewer (with live tool calls in the sidebar)")

# Sidebar: session controls + examples + dev panel
with st.sidebar:
    st.header("Session")
    if st.button("🔄 Reset conversation"):
        st.session_state.clear()
        st.rerun()

    st.subheader("Try these prompts")
    st.code("Plan a week-long Europe trip for a student on a $1,500 budget who loves history and food")
    st.code("3-day Paris trip for art lovers with $800 budget")

    st.subheader("Developer view")
    show_tools = st.toggle("Show tool activity (live)", value=True)
    if show_tools:
        tool_expander = st.expander("🔧 Tool activity", expanded=True)
        tool_panel = tool_expander.container()
    else:
        tool_panel = st.container()  # inert sink

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # list[dict(role, content)]
if "meta" not in st.session_state:
    st.session_state.meta = []      # list[dict(trace)]

# Render history
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and i < len(st.session_state.meta):
            meta = st.session_state.meta[i]
            if meta:
                st.caption(meta.get("trace", ""))

# Chat input
user_input = st.chat_input("Describe your travel (destination, duration, budget, interests)…")

if user_input:
    # Add user message to history and render it
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.meta.append(None)
    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant output block
    with st.chat_message("assistant"):
        # Live “working…” text and progress bar
        live_msg = st.empty()
        progress = st.progress(0)

        # Per-request tool log (shown in the sidebar)
        tool_events: List[Dict[str, Any]] = []

        def ui_tool_logger(event: Dict[str, Any]) -> None:
            """Append an event and re-render the sidebar log."""
            tool_events.append(event)
            with tool_panel:
                st.markdown("**Recent tool calls**")
                for ev in tool_events[-60:]:  # last N entries
                    t = ev.get("tool", "unknown")
                    et = ev.get("type", "event")
                    if et == "call":
                        st.write(f"• **{t}** called with `{ev.get('args')}`")
                    elif et == "result":
                        st.write(f"• **{t}** result preview:\n\n> {ev.get('preview')}")
                    elif et == "error":
                        st.error(f"• **{t}** error: {ev.get('error')}")
                    elif et == "end":
                        st.write(f"• **{t}** finished")

        # Install the logger so tools can report to the sidebar
        set_tool_logger(ui_tool_logger)

        try:
            # Optional: clear sidebar panel on each run
            with tool_panel:
                st.empty()

            # Step 1: Planner
            with st.status("🧭 Planner Agent: generating itinerary…", expanded=True) as status:
                live_msg.markdown("🧭 Planner Agent is creating your itinerary…")
                plan_text = run_planner(user_input)
                progress.progress(40)
                status.update(label="🔎 Reviewer Agent: validating with live searches…", state="running")

            # Step 2: Reviewer (tool calls will appear live in sidebar)
            live_msg.markdown("🔎 Reviewer Agent is validating the plan with live searches…")
            review_text = run_reviewer(plan_text)
            progress.progress(90)

            # Completed
            live_msg.markdown("✅ Validation complete. Rendering results…")
            time.sleep(0.2)
            progress.progress(100)

            # Final render: show only the validated result, with the raw plan expandable
            st.info("🤖 **Reviewer Agent** (validated)")
            st.markdown(review_text)
            with st.expander("See raw plan from Planner Agent"):
                st.markdown(plan_text)

            # Save only the validated result to history
            st.session_state.messages.append({"role": "assistant", "content": review_text})
            st.session_state.meta.append({"trace": "Planner Agent → Reviewer Agent"})
            st.caption("Planner Agent → Reviewer Agent")

        except Exception as e:
            # Friendly error box
            live_msg.markdown("❌ Something went wrong.")
            err = f"⚠️ Error while processing your request:\n\n```\n{e}\n```"
            st.markdown(err)
            st.session_state.messages.append({"role": "assistant", "content": err})
            st.session_state.meta.append({"trace": "Runtime error."})

        finally:
            # Always remove the logger so it doesn't leak into the next request
            set_tool_logger(None)