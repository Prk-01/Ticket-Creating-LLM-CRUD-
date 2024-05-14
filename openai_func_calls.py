import openai
from openai import OpenAI
import json
from crud_openai_func import get_read_ticket_fn,get_create_ticket_fn,get_update_ticket_fn,get_delete_ticket_fn


#Ticket bot creation
class TicketBot:
    def __init__(self, db,key):
        # default prompt for bot
        self.client=OpenAI(api_key=key)
        self.default = [{
            "role": "system",
            "content": """
            
            1)You are a bot who creates pages for user problems, your able to create,update,read and delete user ticket.

            2)You're job is to just handle pages like ticket creation, ticket deletion etc.,nothing more than
            ticket handling and also answer users within 100 words or less.

            3)You can delete tickets.
            
            4)Make sure to provide ticket number when a ticket is created. The ticket number is really important.

            """
        },]
        self.db = db

    def chat(self, query):
        ticket_track=None
        response = self.make_openai_request(query)
        message = response.choices[0].message

        #if users requests a ticket operation
        if (hasattr(message, 'function_call') & (message.function_call != None)):
            function_name = message.function_call.name
            arguments = json.loads(message.function_call.arguments)
            if function_name == "create_ticket":
                function_response,ticket_track = getattr(self, function_name)(**arguments)
            else:
                function_response = getattr(self, function_name)(**arguments)
            #re-send info for bot summarized output
            if not message.content:
                message.content=function_response
            system_response = self.make_system_request(query[-1], message, function_name, function_response)
            system_message = system_response.choices[0].message
            return system_message,ticket_track

        return message,ticket_track


    #initial openai request for query
    def make_openai_request(self,memory):
        memory=self.default+memory
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            temperature=0,
            messages=memory,
            functions=[get_create_ticket_fn, get_read_ticket_fn, get_delete_ticket_fn, get_update_ticket_fn],
        )
        return response

    # follow call for openai
    def make_system_request(self, query, message, function_name, function_response):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            temperature=0,
            messages=[
                {"role": "user", "content": query['content']},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return response

    # Ticket read function, not alot of error handling has openai handles if function returns None
    def read_ticket(self, ticket_id=None):
        if ticket_id:
            return "This is the information of your ticket" + str(self.db.find_one({"ticket_id": ticket_id}))
        return "I apologize I couldn't find your ticket, I request to re-check your ticket number and status."


    #Ticket delete function
    def delete_ticket(self, ticket_id=None):
        if ticket_id:
            self.db.delete_one({"ticket_id": ticket_id})
            return f"your ticket of number '{ticket_id}' is successfully deleted"
        return "I apologize I couldn't find your ticket, I request to re-check your ticket number and status."

    #Ticket creation, based on information fetched and summarized by openai
    def create_ticket(self, ticket_title, ticket_description, ticket_priority="low"):
        try:
            ticket = {}
            ticket["ticket_id"] = 'ayz' + str(self.db.estimated_document_count() + 1)
            ticket["ticket_title"] = ticket_title
            ticket["ticket_description"] = ticket_description
            ticket["ticket_priority"] = ticket_priority
            self.db.insert_one(ticket)

            return f'''Thank you, We have all your information we will contact you soon for assisting you in your problems, 
            your ticket number is "{ticket["ticket_id"]}". 
            Please remember ticket number as is it important for further support reference''',{'Ticket created':ticket["ticket_id"]}
        except Exception as e:
            return "I Apologize, Database down ticket could not be created",None

    #Ticket update based on ticket_id // should work on update by dynamic features
    def update_ticket(self, ticket_id=None, ticket_title=None, ticket_description=None, ticket_priority=None):
        if ticket_id:
            ticket_data = self.db.find_one({"ticket_id": ticket_id})
            del ticket_data['_id']
            updated = []
            user_data = locals()
            for i in ticket_data.keys():
                if user_data[i] != None:
                    ticket_data[i] = user_data[i]
                    updated.append(i)
            self.db.update_one({"ticket_id": ticket_id}, {"$set": ticket_data})
            return f"Ticket updated successfully, You updated {str(updated)}"
        return "I apologize I couldn't find your ticket, I request to re-check your ticket number and status."


