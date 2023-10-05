import os
from typing import Callable
from .subprocess_tool import SubProcessTool
from tools_manager.utils import _load_file,utf8
from prompts import PromptsManager
from protocol import Message
class ToolsManager:
    def __init__(self, base_dir: str,memento_factory: Callable = None):
        self.tools = {}
        self.base_dir = base_dir
        self.memento_factory = memento_factory
        self.load_tools()
    
    def load_tools(self):
        # Each tool is a directory in the base directory
        for tool in os.listdir(self.base_dir):
            tool = tool.strip()
            if tool=="" or tool == "." or tool == ".." or tool.startswith("_"):
                continue
            if os.path.isdir(os.path.join(self.base_dir, tool)):
                    # If the directory contains a file called "run" then it is a subprocess tool.
                    # If it contains a file called start.txt, then it is a memento tool
                    # otherwise we have an error.
                    if os.path.isfile(os.path.join(self.base_dir, tool, "run")):
                        self.tools[tool] = SubProcessTool(tool, self.base_dir)
                    elif os.path.isfile(os.path.join(self.base_dir, tool, "start.txt")):
                        tool_base_dir = os.path.join(self.base_dir, tool)
                        self.tools[tool] = MementoTool(tool, tool_base_dir, self.memento_factory)

        # The system and user tools are always available
        self.tools["system"] = SystemTool(self)
        self.tools["user"] = UserTool()

    def get_tool(self, tool_name: str):
        return self.tools[tool_name]
    
    def get_tools(self)->list[str]:
        return list(self.tools.keys())
    
    def process_command(self,message: Message) -> tuple[str,str]:
        # The command is in the format {{FROM:memento TO:<tool>}}<command>{{END}}
        # (command can be multi-line)
        # We need to extract the tool name and the command
        command = message.msg_content
        tool_name = message.msg_to
        command = command.strip()
        
        # Process the command
        if tool_name in self.tools:
            return tool_name,self.tools[tool_name].process_command(command)
        else:
            return "system","Unknown tool: " + tool_name
        
     


    
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

        return "Invalid command received.Available commands are:\n list_tools: List all available tools.\nhelp: Get help for a tool."
        
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

class MementoTool:
    def __init__(self, name: str, base_dir: str, memento_factory: Callable):
        
        self.tools_manager = ToolsManager(os.path.join(base_dir, "tools"), memento_factory)
        self.prompts_manager = PromptsManager(base_dir)
        self.memento = memento_factory(self.tools_manager,self.prompts_manager,name)
        self.memento_initialized = False
        self.name = name
        self.description = _load_file(base_dir, ".", "description.txt")
        self.help = _load_file(base_dir, ".", "help.txt")
        
    
    def process_command(self, command: str) -> str:
        if command == "help":
            return self.help
        
        if not self.memento_initialized:
            self.memento.start()
            self.memento_initialized = True
        
        return self.memento.process(command)



   
    
   
        