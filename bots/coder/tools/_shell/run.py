import subprocess
import os
shell = subprocess.Popen(["/bin/bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         cwd="workspace")

MAX_RESULT_LENGTH=256

def format_result(result):
    # If the result is too long, truncate the middle
    if len(result) > MAX_RESULT_LENGTH:
        result = result[:MAX_RESULT_LENGTH//2] + "...(truncated)..." + result[-MAX_RESULT_LENGTH//2:]
    return result

def exec_command(command):
     # Send the command to the tool, adding a newline at the end
    cmdLine = command+" 2>&1; ec=$?;echo ''; echo '{{ENDCOMMAND}}'; echo $ec\n"
    shell.stdin.write(cmdLine.encode("utf-8"))
    shell.stdin.flush()

    # Read the result - it can contain multiple lines
    result = ""
    exit_code = 0
    while True:
        line = shell.stdout.readline().decode("utf-8")
        if line == "{{ENDCOMMAND}}\n":
            exit_code = int(shell.stdout.readline().decode("utf-8"))
            break
        result = result + line

    result = format_result(result.strip())
    return result,exit_code


def exec_commands(commands):
     for command in commands:
        output,exit_code = exec_command(command)
        print(f"Command: {command}, Exit code: {exit_code}")
        if output and output != "":
            print(f"Output:\n {output}")
        else:
            print("No output")
        print("==")
        if exit_code != 0:
            break

     print("{{ENDCOMMAND}}")
                           
# Loop to read a command from stdin, one command per line
in_command = False
commands=[]


while True:
    command = input("")
    if command == "exit":
        break
    command = command.strip()
    if command == "{{BEGINCOMMAND}}":
        in_command = True
        continue
    if command == "{{ENDCOMMAND}}":
        exec_commands(commands)
        commands=[]
        in_command = False
        continue
    if in_command:
        commands.append(command)
    

    
    