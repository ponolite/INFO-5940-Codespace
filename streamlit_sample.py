import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Hello IFO-5940", layout="centered")

st.title("👋 Hello from INFO-5940")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You're a knowledgeable cook"},
                                    {"role": "assistant", "content": "Hello! I'm here to help you!"}]
# st.session_state["messages"].append([{"role": "assistant, "content": "Howdy!"}])     

for msg in st.session_state.messages:
    if msg['role'] != 'system':
        st.chat_message(msg['role']).write(msg['content'])

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

if prompt := st.chat_input():
    client = OpenAI()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(model="openai.gpt-4o",
                                            #    messages = [{"role": "system", "content": "You're a knowledgeable cook."},
                                            #                {"role": "assistant", "content": "Hello! I'm here to help you!"}],
                                               messages=st.session_state.messages,
                                               stream=True)
        response = st.write_stream(stream)
    
    # st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})