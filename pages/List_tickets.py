import streamlit as st
import os
# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv())
from pymongo import MongoClient

#DB connection
db_uri=st.secrets["MONGODB_URI"]
mongodb_client = MongoClient(db_uri)
database = mongodb_client.tickets
ticketdb=database.ticketdb

#simple page config
st.set_page_config(
    page_title="tickets",
    page_icon="🎫"
)

#Get all tickets and display
tickets=ticketdb.find({})
for ticket in tickets:
    expander = st.expander(f"Ticket Number : 🎫'{ticket['ticket_id']}'")
    expander.write(f'''
        Ticket Title : {ticket['ticket_title']}\n
        Ticket Description : {ticket['ticket_description']}\n
        Ticket Priority : {ticket['ticket_priority']}
    ''')



