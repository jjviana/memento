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


settings = Settings()
api_key = settings.get("openai_api_key")
if api_key is None or api_key == "":
    openai.api_key = prompt("Please enter your OpenAI API key: ")
    settings.set("openai_api_key", openai.api_key)

session = PromptSession(history=FileHistory("history.txt"))
model = LoopDetector(GPT_35(api_key,"gpt3_5.log"))
prompts_manager = PromptsManager(".")
tools_manager = ToolsManager("tools")
starting_prompt = prompts_manager.get_prompt("start")
response = model.initial_prompt(starting_prompt)

def format_tool_output(tool_name, tool_output):
    return "{{FROM:"+tool_name+" TO:assistant}}\n" + tool_output + "\n{{END}}"

while True:

    if response.startswith("{{FROM:assistant TO:"):
        tool_name,tool_output = tools_manager.process_command(response)
        if tool_name == "user":
            print(tool_output)
            user_input = session.prompt(">")
            if user_input == "exit":
                break
            tool_output = user_input
        
        tool_output = format_tool_output(tool_name, tool_output)
        response = model.input(tool_output)
    else:
        if response == LoopDetector.LOOP_DETECTED_SENTINEL:
            print("Loop detected in model response")
            break
        response = model.input(format_tool_output("system","Invalid message format"))



