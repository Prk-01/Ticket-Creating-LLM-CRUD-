import streamlit as st
from openai_func_calls import TicketBot
from pymongo import MongoClient

#Streamlit has Toml env
# import os
# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv())

#database connection config // only for streamlit testing
db_uri=st.secrets["MONGODB_URI"]
mongodb_client = MongoClient(db_uri)
database = mongodb_client.tickets
ticketdb=database.ticketdb

st.set_page_config(
    page_title="ticket bot",
    page_icon="🤖"
)

#Api-key Text box indicator // for streamlit only
def highlight(color):
    styl = f"""
    <style>
        input[type="password"] {{
          background-color:{color};
        }}
    </style>
    """
    st.markdown(styl, unsafe_allow_html=True)

#Get user api-key // for streamlit demo only
def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key ", placeholder="Ex: sk-2twmA8tfCb8un4...",
                                   key="openai_api_key_input", type="password")
    highlight(" ")
    return input_text

openai_api_key= get_openai_api_key()

#To maintain model instance as local chat history of streamlit is not in sync with models
if 'flag' not in st.session_state:
    st.session_state['flag'] = True

#Title
st.header("Ticket bot")

#streamlit chat session history
#Not with sync with model context has model context requires vector db implementation
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


#prompt limited to less than 250 charcters// 250 -> just a random number
if prompt := st.chat_input("Have an issue? Create a ticket help is here!"):
    highlight(" ")
    if len(prompt)>250:
        st.warning("Please state your problems within 100-150 words")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Simple error handling for streamlit demo
            if openai_api_key:
                try:
                    if st.session_state['flag']:
                        st.session_state['flag'] = False
                        bot=TicketBot(ticketdb,openai_api_key)
                    response = bot.chat(prompt).content
                except Exception as e:
                    st.session_state['flag'] = True
                    #Check API is valid!
                    if 'Incorrect API' in str(e):
                        response="Please Enter a valid Openai API Key"
                        highlight("#DE583E")
                    else:
                        response = "Application error please refresh or re-check your request!"
            else:
                response="Missing Openai API key on above text box"
                highlight("#DE583E")
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        #chat history reduction // has model may not maintain many contexts
        if len(st.session_state.messages) >8:
            st.session_state.messages=st.session_state.messages[-8:]
            st.session_state.messages.insert(0,{"role": "assistant", "content": "Previous chats are detached!"})





