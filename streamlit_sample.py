import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Hello IFO-5940", layout="centered")

st.title("👋 Hello from INFO-5940")

# Read knowledge base from data/important_knowledge.txt
with open('data/important_knowledge.txt', 'r') as file:
     knowledge_base = file.read()

if "messages" not in st.session_state: # Store the main states that the bot can be in, set the system knowledge, the user main request, and the opening assistant's line
    st.session_state["messages"] = [{"role": "system", "content": "You're a knowledgeable cook"},
                                    {"role": "user", "content": "I want you to answer questions based on this knowledge base: " + knowledge_base},
                                    {"role": "assistant", "content": "Hello! I'm here to help you!"}]
# st.session_state["messages"].append([{"role": "assistant, "content": "Howdy!"}])     

for msg in st.session_state.messages: # Run through the items in st.session_state, if they aren't system (don't write the contents in the system) and the user's content, then write according to the bot's knowledge
    if msg['role'] != 'system' and msg['content'] != "I want you to answer questions based on this knowledge base: " + knowledge_base: 
        st.chat_message(msg['role']).write(msg['content'])

# and  msg['content'] != "I want you to answer questions based on this knowledge base" + knowledge_base:

# if globals().get('page_title') is None:
#     page_title = "👋 Hello from INFO-5940!"

# st.write("If you can see this page, Streamlit is running correctly inside your Codespace.")

# name = st.text_input("What is your name?")
# if name:
#     st.success(f"Nice to meet you, {name}!")
#     page_title = "We're one testin"

# st.markdown("---")
# st.caption("This is a test app for INFO 5940 Fall 2025.")


# Way to run streamlit
# streamlit run streamlit_sample.py

if prompt := st.chat_input(): # Create the chat interface
    client = OpenAI() # Call API

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(model="openai.gpt-4o", # Specify model
                                            #    messages = [{"role": "system", "content": "You're a knowledgeable cook."},
                                            #                {"role": "assistant", "content": "Hello! I'm here to help you!"}],
                                               messages=st.session_state.messages, # Print messages according to what's set in the st.session_state.messages
                                               stream=True) # The API sends back small chunks (tokens) as soon as they’re generated, seems like typing
        response = st.write_stream(stream)
    
    # st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})