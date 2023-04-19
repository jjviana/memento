from abc import ABC,abstractmethod
import hashlib
class LanguageModel(ABC):

    @abstractmethod
    def initial_prompt(self,prompt:str) -> str:
        pass

    @abstractmethod
    def input(self,prompt:str) -> str:
        pass

class LoopDetector(LanguageModel):

    LOOP_DETECTED_SENTINEL = "{{LOOP_DETECTED}}"

    "Detects loops in the conversation"
    def __init__(self,language_model) -> None:
        super().__init__()
        self.language_model = language_model
        self.history = []
        self.history_size = 10

    def initial_prompt(self,prompt:str) -> str:
    
        response = self.language_model.initial_prompt(prompt)
        # hash the response
        hashed_response = hashlib.md5(response.encode()).hexdigest()
        # add the response to the history
        self.append_response(hashed_response)
        return response
    
    def input(self,prompt:str) -> str:
        response = self.language_model.input(prompt)
        # hash the response
        hashed_response = hashlib.md5(response.encode()).hexdigest()
        # add the response to the history
        self.append_response(hashed_response)
       
       # If any response repeats more than 7 times, return a special message
        for h in self.history:
           if self.history.count(h) > 7:
               return self.LOOP_DETECTED_SENTINEL
           
        return response
           
    def append_response(self,response:str):
        self.history.append(response)
        if len(self.history) > self.history_size:
            self.history.pop(0)