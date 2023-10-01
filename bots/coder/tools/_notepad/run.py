import os
import datetime

MAX_RESULT_LENGTH=2048

def print_help():
    with open("../help.txt","r") as f:
        print(f.read())


def exec_commands(first_line,remaining_lines):
    if first_line == "help":
        print_help()
    else:
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        note_name=f"note_{now}.txt"
        with open(note_name,"w") as f:
            f.write(first_line + "\n")
            f.write(remaining_lines)
        print("Ok, I have saved your note")

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
    

    
    