import os
import openai
from prompt_toolkit import prompt
from settings import Settings
from prompts import PromptsManager
from language_models import GPT_35,BedrockClaude
from language_models import LoopDetector
from language_models import Message
from language_models import OpenAIEmbeddingModel
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from tools_manager import ToolsManager
import argparse

class Memento:
    def __init__(self, tools_manager, prompts_manager,model,logger):
        self.tools_manager = tools_manager
        self.prompts_manager = prompts_manager
        self.model = model
        self.logger = logger
        self.model.set_gc_manager(self.manage_gc)
        self.session_cost = 0.0
        self.iteraction_costs = []
    
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

        interaction_cost = 0.0
        while True:
            response = response.lstrip()
            messages = self.model.get_messages()
            response_cost = messages[-1].cost
            interaction_cost = interaction_cost + response_cost
        
            if response.startswith("{{FROM:memento TO:"):
                tool_name,tool_output = self.tools_manager.process_command(response)
                if tool_name == "user":
                    #self.check_update_memory()
                    self.session_cost = self.session_cost + interaction_cost
                    self.iteraction_costs.append(interaction_cost)
                    return tool_output

                tool_output = self.format_tool_output(tool_name, tool_output)
                response = self.model.input(tool_output)

            else:
                if response == LoopDetector.LOOP_DETECTED_SENTINEL:
                    response = self.model.input(self.format_tool_output("system","You are repeating yourself. Please check for any error messages, check command syntax or try a different approach."))  
                else:
                    print(f"Invalid response:-{response}")
                    response = self.model.input(self.format_tool_output("system"," Your last message is not formatted correctly. Please repeat it with the correct format."))

    def manage_gc(self,model):
       
        raise NotImplementedError("Maximum tokens used.")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Model type must be OpenAI or BedrockClaude
    parser.add_argument("--model", type=str, required=True, help="Model type")

    language_model_factory = None
    if parser.parse_args().model == "OpenAI":
        settings = Settings()
        api_key = settings.get("openai_api_key")
        if api_key is None or api_key == "":
            openai.api_key = prompt("Please enter your OpenAI API key: ")
            settings.set("openai_api_key", openai.api_key)
        def gpt_35_factory(logger):
            return GPT_35(api_key,logger)
        language_model_factory = gpt_35_factory

    elif parser.parse_args().model == "BedrockClaude":
        def bedrock_claude_factory(logger):
            return BedrockClaude("anthropic.claude-v2",logger)
        language_model_factory = bedrock_claude_factory
    else:
        raise ValueError("Model type must be OpenAI or BedrockClaude")

    session = PromptSession(history=FileHistory("history.txt"))

    log_file= open("memento.log", "a")
    def log(message: str):
        log_file.write(message + "\n")
        log_file.flush()
    def logger(instance: str):
        return lambda message: log(instance+"->"+message)

    prompts_manager = PromptsManager(".")

    def new_memento(tools_manager,prompts_manager,instance: str):
        model = LoopDetector(language_model_factory(logger(instance)))
        return Memento(tools_manager,prompts_manager,model,logger(instance))


    tools_manager = ToolsManager("tools",new_memento)


    top_level_memento = new_memento(tools_manager,prompts_manager,"top_level")
    response = top_level_memento.start()

    while True:
        print(response)
        iteraction_cost = "{:.6f}".format(top_level_memento.iteraction_costs[-1])
        session_cost = "{:.6f}".format(top_level_memento.session_cost)
        print(f"====\nIteraction cost: {iteraction_cost}\nSession cost: {session_cost}\n====")
        message = session.prompt(">")
        response = top_level_memento.process(message)
