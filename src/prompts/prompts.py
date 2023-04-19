import os

class PromptsManager:

    def __init__(self,bot_dir) -> None:
        self.bot_dir = bot_dir
    
    def get_prompt(self,prompt_name:str) -> str:
        prompt_path = os.path.join(self.bot_dir,prompt_name+".txt")
        with open(prompt_path) as f:
            return f.read()
    