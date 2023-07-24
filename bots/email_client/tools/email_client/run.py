from simplegmail import Gmail
from simplegmail.query import construct_query

MAX_RESULT_LENGTH=2048

def print_help():
    with open("help.txt","r") as f:
        print(f.read())

gmail = Gmail()
def exec_commands(first_line,remaining_lines):
    args=first_line.strip().split(" ")
    command = args[0]
    if command == "list_unread":
        # Unread messages in your inbox
        query_params = {
            "newer_than": (1, "day"),
            "unread": True
        }
        messages = gmail.get_messages(query=construct_query(query_params))
        for message in messages:
            print(f"ID: {message.id}")
            print(f"From: {message.sender}")
            print(f"Subject: {message.subject}")
            print(f"Date: {message.date}")
            print("====")
    else:
        if command == "get_message":
            message_id = args[1].strip()
            query_params = {
            "newer_than": (1, "day"),
            "unread": True
            }
            messages = gmail.get_messages(query=construct_query(query_params))
            for message in messages:
                if message.id == message_id:
                    print(f"ID: {message.id}")
                    print(f"From: {message.sender}")
                    print(f"Subject: {message.subject}")
                    print(f"Date: {message.date}")
                    print("Body:\n====")
                    if message.plain is not None:
                        print(message.plain[:MAX_RESULT_LENGTH])
                    else:
                        print(message.html[:MAX_RESULT_LENGTH])
                        
                    print("====")
                    print("Attachments:\n====")
                    for attachment in message.attachments:
                        print(f"Name: {attachment.filename}")
                        print(f"Type: {attachment.filetype}")
                        print("====")
                    break


        else:
            print("Unknown command")
            print_help()

    print("{{ENDCOMMAND}}")
                           
in_command = False
first_line = ""
remaining_lines = ""
while True:
    line = input("")
    strip_line = line.strip()
    if strip_line == "{{BEGINCOMMAND}}":
        in_command = True
        continue
    if strip_line == "{{ENDCOMMAND}}":
        exec_commands(first_line,remaining_lines)
        first_line = ""
        remaining_lines = ""
        in_command = False
        continue
    if in_command:
        if first_line == "":
            first_line = strip_line
        else:
            remaining_lines = remaining_lines + line + "\n"
    

    
    