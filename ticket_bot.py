import streamlit as st
import os
# from dotenv import load_dotenv, find_dotenv
from openai_func_calls import TicketBot
from pymongo import MongoClient
# _ = load_dotenv(find_dotenv())
# openai_api_key = os.environ["OPENAI_API_KEY"]
openai_api_key=st.secrets["OPENAI_API_KEY"]
db_uri=st.secrets["MONGODB_URI"]
mongodb_client = MongoClient(db_uri)
database = mongodb_client.tickets
ticketdb=database.ticketdb

st.set_page_config(
    page_title="ticket bot",
    page_icon="🤖"
)


st.title("Ticket bot")
# Simple implementation for application demo in testing
st.warning("Note this a demo application under testing you can only run 10 requests")

#Session for limiting openai queries
if 'key' not in st.session_state:
    st.session_state['key'] = 10

#streamlit chat session history
#not syncing chat history with streamlit session history and bot as this for testing and working on full_stack feature
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#prompt limited to less than 250 charcters
if prompt := st.chat_input("Have an issue? Create a ticket help is here!"):
    if len(prompt)>250:
        st.warning("Please state your problems within 100-150 words")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if st.session_state['key']>0:
                bot=TicketBot(ticketdb)
                response = bot.chat(prompt).content
                st.session_state['key'] -= 1
            else:
                response="Your limit has been reached!"
            print(st.session_state['key'])
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        #chat history reduction
        if len(st.session_state.messages) >8:
            st.session_state.messages=st.session_state.messages[-8:]
            st.session_state.messages.insert(0,{"role": "assistant", "content": "Previous chats are detached!"})

