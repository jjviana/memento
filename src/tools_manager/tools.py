import os
import subprocess
class ToolsManager:
    def __init__(self, base_dir: str):
        self.tools = {}
        self.base_dir = base_dir
        self.load_tools()
    
    def load_tools(self):
        # Each tool is a directory in the base directory
        for tool in os.listdir(self.base_dir):
            tool = tool.strip()
            if tool=="" or tool == "." or tool == ".." or tool.startswith("_"):
                continue
            if os.path.isdir(os.path.join(self.base_dir, tool)):
                    self.tools[tool] = Tool(tool, self.base_dir)

        # The system and user tools are always available
        self.tools["system"] = SystemTool(self)
        self.tools["user"] = UserTool()

    def get_tool(self, tool_name: str):
        return self.tools[tool_name]
    
    def get_tools(self)->list[str]:
        return list(self.tools.keys())
    
    def process_command(self,command: str) -> tuple[str,str]:
        # The command is in the format {{FROM:assistant TO:<tool>}}<command>{{END}}
        # (command can be multi-line)
        # We need to extract the tool name and the command
        # check if the message is really from the assistant
        if not command.startswith("{{FROM:assistant TO:"):
            return "system","Invalid format"
        
        tool_name = command[command.find("TO:")+3:command.find("}}")]
        command = command[command.find("}}")+2:]
        command = command[:command.find("{{END}}")]
        command = command.strip()
        
        # Process the command
        if tool_name in self.tools:
            return tool_name,self.tools[tool_name].process_command(command)
        else:
            return "system","Unknown tool: " + tool_name
        
        
    
def utf8(s):
        return s.encode('utf-8')

class Tool:

    BEGIN_COMMAND_SENTINEL="{{BEGINCOMMAND}}"
    ENDCOMMAND_SENTINEL="{{ENDCOMMAND}}"

    def __init__(self, name: str, base_dir: str):
        self.name = name
        self.base_dir = base_dir
        self.subprocess = None
        
        # Each tool has a description file (description.txt) and a help file (help.txt)
        self.description = self._load_file("description.txt")
        self.help = self._load_file("help.txt")

   
    
    def process_command(self, command: str) -> str:
        
        if command == "help":
            return self.help
        
        if self.subprocess is None or self.subprocess.poll() is not None:
            self.subprocess = subprocess.Popen([os.path.join(self.base_dir,self.name, "run")], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Send the command to the tool
        self.subprocess.stdin.write(utf8("\n"+Tool.BEGIN_COMMAND_SENTINEL+"\n"))
        self.subprocess.stdin.write(utf8((command)))
        self.subprocess.stdin.write(utf8("\n"+Tool.ENDCOMMAND_SENTINEL+"\n"))
        self.subprocess.stdin.flush()

        # Read the result - it can contain multiple lines
        result = ""
        while True:
            line = self.subprocess.stdout.readline().decode("utf-8")
            if line.strip() == Tool.ENDCOMMAND_SENTINEL:
                break
            result = result + line
        
        return result
     
        
        
    def _load_file(self, file_name: str) -> str:
        with open(os.path.join(self.base_dir, self.name, file_name), "r") as f:
            return f.read()
    
class SystemTool:

    def __init__(self,manager: ToolsManager):
        self.manager = manager
        self.description = "Used to interact with the system"
        self.help = "Available commands are:\n list_tools: List all available tools.\nhelp: Get help for a tool."

    def process_command(self, command: str) -> str:
        if command == "list_tools":
            return self._list_tools()
        else: 
            # Help can be requested for any tool
            if command.startswith("help "):
                tool_name = command[5:]
                if tool_name in self.manager.get_tools():
                    return self.manager.get_tool(tool_name).help
                else:
                    return "Available commands are:\n list_tools: List all available tools.\nhelp: Get help for a tool."
            else:
                if command == "help":
                    return self.help

        return "Available commands are:\n list_tools: List all available tools.\nhelp: Get help for a tool."
        
    def _list_tools(self) -> str:
        result = "Available tools:\n"
        for tool in self.manager.get_tools():
            result = result + tool + ": " + self.manager.get_tool(tool).description + ".\n"
        return result
    
class UserTool:
    def __init__(self):
       self.description = "Used to send and receive messages to the user"
       self.help="Just send your message to the user."
    
    def process_command(self, command: str) -> str:
       return command
    
   
    
   
        