import streamlit as st
import os
# from dotenv import load_dotenv, find_dotenv
from openai_func_calls import TicketBot
from pymongo import MongoClient
# _ = load_dotenv(find_dotenv())
# openai_api_key = os.environ["OPENAI_API_KEY"]
# os.environ['OPENAI_API_KEY']=st.secrets["OPENAI_API_KEY"]
db_uri=st.secrets["MONGODB_URI"]
mongodb_client = MongoClient(db_uri)
database = mongodb_client.tickets
ticketdb=database.ticketdb

st.set_page_config(
    page_title="ticket bot",
    page_icon="🤖"
)

# Simple implementation for application demo in testing

#Session for limiting openai queries
# if 'key' not in st.session_state:
#     st.session_state['key'] = 10

#Api-key Text box highlight
def highlight(color):
    styl = f"""
    <style>
        input[type="password"] {{
          background-color:{color};
        }}
    </style>
    """
    st.markdown(styl, unsafe_allow_html=True)

#get User api_key
def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key ", placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    highlight(" ")
    if input_text:
        os.environ["OPENAI_API_KEY"] = input_text
    return input_text

openai_api_key = get_openai_api_key()

st.title("Ticket bot")

#streamlit chat session history
#not syncing chat history with streamlit session history and bot as this for testing and working on full_stack feature
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#prompt limited to less than 250 charcters
if prompt := st.chat_input("Have an issue? Create a ticket help is here!"):
    highlight(" ")
    if len(prompt)>250:
        st.warning("Please state your problems within 100-150 words")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if openai_api_key:
            # if st.session_state['key']>0:
                try:
                    bot=TicketBot(ticketdb)
                    response = bot.chat(prompt).content
                    # st.session_state['key'] -= 1
                except Exception as e:
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
        #chat history reduction
        if len(st.session_state.messages) >8:
            st.session_state.messages=st.session_state.messages[-8:]
            st.session_state.messages.insert(0,{"role": "assistant", "content": "Previous chats are detached!"})

