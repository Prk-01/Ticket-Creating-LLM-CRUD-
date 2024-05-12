from openai_function_calling import Function,Parameter,FunctionDict

#create_ticket function_calling_schema
create_ticket_fn = Function(
    "create_ticket",
    "Create Ticket based on the user problems",
    [
        Parameter(
            "ticket_title",
            "string",
            "Title of the user problem for the ticket"
        ),
        Parameter(
            "ticket_description",
            "string",
            "Details of the user problem for the ticket"
        ),
        Parameter(
            "ticket_priority",
            "string",
            '''High priority for issues that need help now, intermediate priority for problems that 
            need help within a week and low priority for problems more than a week''',
            enum=['High', 'Intermediate', 'Low'],
        ),
    ],
)

#read_ticket function_calling_schema
read_ticket_fn = Function(
    "read_ticket",
    "Get details of a user ticket based on their ticket information",
    [
        Parameter(
            "ticket_id",
            "string",
            "Unique Number of the ticket to get its information"
        ),
    ],
)

#delete_ticket function_calling_schema
delete_ticket_fn = Function(
    "delete_ticket",
    "When the user wants to delete or withdraw their ticket",
    [
        Parameter(
            "ticket_id",
            "string",
            "Unique Number of the ticket to delete or withdraw it"
        )
    ]
)

#update_ticket function_calling_schema
update_ticket_fn = Function(
    "update_ticket",
    "This function is used to update or change Ticket based on the user request",
    [
        Parameter(
            "ticket_id",
            "string",
            "Unique Number of the ticket to delete or withdraw it"
        ),

        Parameter(
            "ticket_title",
            "string",
            "Title of the user problem for the ticket"
        ),
        Parameter(
            "ticket_description",
            "string",
            "Details of the user problem for the ticket"
        ),
        Parameter(
            "ticket_priority",
            "string",
            "Priority as High, intermediate or low based on user problem in the ticket",
            enum=['High', 'Intermediate', 'Low'],
        ),
    ],
)

#Genreate Json version of CRUD functions
get_create_ticket_fn: FunctionDict = create_ticket_fn.to_dict()
get_read_ticket_fn: FunctionDict = read_ticket_fn.to_dict()
get_delete_ticket_fn: FunctionDict = delete_ticket_fn.to_dict()
get_update_ticket_fn: FunctionDict = update_ticket_fn.to_dict()

#Gets updated by ticket_id for now // Need dynamic capture of ticket
get_update_ticket_fn['parameters']['required']=["ticket_id"]