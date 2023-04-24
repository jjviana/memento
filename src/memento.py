import os
import openai
from prompt_toolkit import prompt
from settings import Settings
from prompts import PromptsManager
from language_models import GPT_35
from language_models import LoopDetector
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from tools_manager import ToolsManager

class Memento:
    def __init__(self, tools_manager, prompts_manager, model):
        self.tools_manager = tools_manager
        self.prompts_manager = prompts_manager
        self.model = model

    def format_tool_output(self, tool_name, tool_output):
        return "{{FROM:"+tool_name+" TO:assistant}}\n" + tool_output + "\n{{END}}"

    def start(self) -> str:
        starting_prompt = self.prompts_manager.get_prompt("start")
        response = self.model.initial_prompt(starting_prompt)
        return self.process_response(response)
    
    def process(self,message:str) -> str:
        
        response = self.model.input(self.format_tool_output("user",message))
        return self.process_response(response)
    
    def process_response(self,response:str) -> str:

        while True:
            if response.startswith("{{FROM:assistant TO:"):
                tool_name,tool_output = self.tools_manager.process_command(response)
                if tool_name == "user":
                    return tool_output

                tool_output = self.format_tool_output(tool_name, tool_output)
                response = self.model.input(tool_output)
            else:
                if response == LoopDetector.LOOP_DETECTED_SENTINEL:
                    raise Exception("Loop detected in model response")
                
                response = self.model.input(self.format_tool_output("system","Invalid message format"))

settings = Settings()
api_key = settings.get("openai_api_key")
if api_key is None or api_key == "":
    openai.api_key = prompt("Please enter your OpenAI API key: ")
    settings.set("openai_api_key", openai.api_key)

session = PromptSession(history=FileHistory("history.txt"))


log_file= open("gpt3_5.log", "a") 


def new_memento(tools_manager,prompts_manager,instance: str):
    def logger(message: str):
        log_file.write(instance+"->"+message + "\n")
        log_file.flush()

    model = LoopDetector(GPT_35(api_key,logger))
    return Memento(tools_manager,prompts_manager,model)

tools_manager = ToolsManager("tools",new_memento)
prompts_manager = PromptsManager(".")
top_level_memento = new_memento(tools_manager,prompts_manager,"top_level")
response = top_level_memento.start()

while True:
    print(response)
    message = session.prompt(">")
    response = top_level_memento.process(message)
