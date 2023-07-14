import os
import openai
from prompt_toolkit import prompt
from settings import Settings
from prompts import PromptsManager
from language_models import GPT_35
from language_models import LoopDetector
from language_models import Message
from language_models import OpenAIEmbeddingModel
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from tools_manager import ToolsManager

class Memento:
    def __init__(self, tools_manager, prompts_manager,model,logger):
        self.tools_manager = tools_manager
        self.prompts_manager = prompts_manager
        self.model = model
        self.logger = logger
        self.model.set_gc_manager(self.manage_gc)
    
    def format_tool_output(self, tool_name, tool_output):
        return "{{FROM:"+tool_name+" TO:memento}}\n" + tool_output + "\n{{END}}"

    def start(self) -> str:
        starting_prompt = self.prompts_manager.get_prompt("start")
        response = self.model.initial_prompt(starting_prompt)
        return self.process_response(response)
    
    def process(self,message:str) -> str:
        
        response = self.model.input(self.format_tool_output("user",message))
        return self.process_response(response)
    
    def process_response(self,response:str) -> str:

        while True:
            if response.startswith("{{FROM:memento TO:"):
                tool_name,tool_output = self.tools_manager.process_command(response)
                if tool_name == "user":
                    #self.check_update_memory()
                    return tool_output

                tool_output = self.format_tool_output(tool_name, tool_output)
                response = self.model.input(tool_output)
            else:
                if response == LoopDetector.LOOP_DETECTED_SENTINEL:
                    response = self.model.input(self.format_tool_output("system","You are repeating yourself. Please check for any error messages, check command syntax or try a different approach."))  
                
                response = self.model.input(self.format_tool_output("system"," You seem to have generated a message with an incorrect format. Please repeat the message with the format {{FROM:memento TO:<tool>}}<message>{{END}}"))

    def manage_gc(self,model):
       
        raise NotImplementedError("Maximum tokens used.")

    

            
settings = Settings()
api_key = settings.get("openai_api_key")
if api_key is None or api_key == "":
    openai.api_key = prompt("Please enter your OpenAI API key: ")
    settings.set("openai_api_key", openai.api_key)

session = PromptSession(history=FileHistory("history.txt"))


log_file= open("memento.log", "a") 
def log(message: str):
    log_file.write(message + "\n")
    log_file.flush()
def logger(instance: str):
    return lambda message: log(instance+"->"+message)

prompts_manager = PromptsManager(".")
embedding_model = OpenAIEmbeddingModel(api_key)

def new_memento(tools_manager,prompts_manager,instance: str):
    model = LoopDetector(GPT_35(api_key,logger(instance)))
    return Memento(tools_manager,prompts_manager,model,logger(instance))
    

tools_manager = ToolsManager("tools",new_memento)


top_level_memento = new_memento(tools_manager,prompts_manager,"top_level")
response = top_level_memento.start()

while True:
    print(response)
    message = session.prompt(">")
    response = top_level_memento.process(message)
