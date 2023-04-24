
import subprocess
import os
from .utils import _load_file,utf8

class SubProcessTool:

    BEGIN_COMMAND_SENTINEL="{{BEGINCOMMAND}}"
    ENDCOMMAND_SENTINEL="{{ENDCOMMAND}}"

    def __init__(self, name: str, base_dir: str):
        self.name = name
        self.base_dir = base_dir
        self.subprocess = None
        
        # Each tool has a description file (description.txt) and a help file (help.txt)
        self.description = _load_file(self.base_dir,self.name,"description.txt")
        self.help = _load_file(self.base_dir,self.name,"help.txt")

   
    
    def process_command(self, command: str) -> str:
        
        if command == "help":
            return self.help
        
        if self.subprocess is None or self.subprocess.poll() is not None:
            self.subprocess = subprocess.Popen([os.path.join(self.base_dir,self.name, "run")], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Send the command to the tool
        self.subprocess.stdin.write(utf8("\n"+SubProcessTool.BEGIN_COMMAND_SENTINEL+"\n"))
        self.subprocess.stdin.write(utf8((command)))
        self.subprocess.stdin.write(utf8("\n"+SubProcessTool.ENDCOMMAND_SENTINEL+"\n"))
        self.subprocess.stdin.flush()

        # Read the result - it can contain multiple lines
        result = ""
        while True:
            line = self.subprocess.stdout.readline().decode("utf-8")
            if line.strip() == SubProcessTool.ENDCOMMAND_SENTINEL:
                break
            result = result + line
        
        return result