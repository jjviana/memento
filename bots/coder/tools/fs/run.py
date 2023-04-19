import os

MAX_RESULT_LENGTH=2048
WORKSPACE_DIR="workspace"
os.makedirs(WORKSPACE_DIR,exist_ok=True)
os.chdir(WORKSPACE_DIR)

def format_list_dir(basedir,result):
    # Format the result of os.listdir
    # returning a string with the list of files and directories
    # and their type (d for directory, f for file) and size
    result_list=""
    for item in result:
        item = os.path.join(basedir,item)
        if os.path.isdir(item):
            result_list=result_list + "d " + item + "\n"
        else:
            result_list=result_list + "f " + item + " " + str(os.path.getsize(item)) + "\n"
    
    return result_list

def exec_commands(first_line,remaining_lines):
    comp = first_line.split(" ")
    if len(comp) < 2:
        print("Invalid command syntax (expected <command> <filename>)")
        return
    command = comp[0]
    filename = comp[1]
    filename=filename.strip()
    if filename.count("=")>0:
        # Remove anything before the first =
        filename = filename[filename.find("=")+1:]

    if command == "write_file":
        content = remaining_lines
        filedir = os.path.dirname(filename)
        if filedir!="":
            os.makedirs(filedir,exist_ok=True)
        with open(filename,"w") as f:
            try:
                f.write(content)
            except Exception as e:
                print(f"Error writing file {filename}: {e}")
                return

            print(f"File {filename} written")

    elif command == "read_file":
        try:
            with open(filename,"r") as f:
                result = f.read()
                if len(result) > MAX_RESULT_LENGTH:
                    result = result[:MAX_RESULT_LENGTH] + "..."
                print(f"File {filename} contents:\n{result}")
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            
    elif command == "delete_file":
        try:
            os.remove(filename)
            print(f"File {filename} deleted")
        except Exception as e:
            print(f"Error deleting file {filename}: {e}")
        
    elif command == "create_directory":
        try:
            os.makedirs(filename,exist_ok=True)
            print(f"Directory {filename} created")
        except Exception as e:
            print(f"Error creating directory {filename}: {e}")

    elif command == "delete_directory":
        try:
            os.removedirs(filename)
            print(f"Directory {filename} deleted")
        except Exception as e:
            print(f"Error deleting directory {filename}: {e}")
    elif command == "list_directory":
        result = []
        try:
            result = os.listdir(filename)
            result_list=format_list_dir(filename,result)
            print(f"Directory {filename} contents:\n{result_list}")
        except Exception as e:
            print(f"Directory {filename} not found: {e}")
    elif command == "move_file":
        if len(comp) < 3:
            print("Invalid command syntax (expected move_file <filename> <new_filename>)")
        else: 
            new_filename = comp[2]
            new_filename=new_filename.strip()
            # If new file is a directory, move the file to that directory
            if os.path.isdir(new_filename):
                new_filename = os.path.join(new_filename,os.path.basename(filename))
            try:
                os.rename(filename,new_filename)
                print(f"File {filename} moved to {new_filename}")
            except Exception as e:
                print(f"Error moving file {filename} to {new_filename}: {e}")
    else:
        print("Unknown command: " + command)
    

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
    

    
    