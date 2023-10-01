from abc import ABC,abstractmethod
import hashlib
from typing import Callable


class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
        self.tokens_used = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.cost = 0.0
        

    def __str__(self):
        return f"{self.role}:{self.content}"

    def __repr__(self):
        return str(self)
    
    def format(self):
        return {
            "role": self.role,
            "content": self.content
        }


class LanguageModel(ABC):

    @abstractmethod
    def initial_prompt(self,prompt:str,need_reply=True) -> str:
        pass
    

    @abstractmethod
    def input(self,prompt:str) -> str:
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_messages(self) -> list[Message]:
        pass

    @abstractmethod
    def set_messages(self,messages:list[Message]):
        pass

    @abstractmethod
    def set_gc_manager(self,gc_manager: Callable):
        pass

    @abstractmethod
    def set_end_marker(self,end_marker: str):
        pass


class LoopDetector(LanguageModel):

    LOOP_DETECTED_SENTINEL = "{{LOOP_DETECTED}}"

    "Detects loops in the conversation"
    def __init__(self,language_model) -> None:
        super().__init__()
        self.language_model = language_model
        self.history = []
        self.history_size = 10

    def initial_prompt(self,prompt:str,need_reply=True) -> str:
    
        response = self.language_model.initial_prompt(prompt,need_reply)
        if need_reply:
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

    def reset(self):
        self.language_model.reset()
        self.history = []

    def get_messages(self) -> list[Message]:
        return self.language_model.get_messages()
    
    def set_messages(self,messages:list[Message]):
        self.language_model.set_messages(messages)

    def set_gc_manager(self,gc_manager: Callable):
        self.language_model.set_gc_manager(gc_manager)

    def set_end_marker(self,end_marker: str):
        self.language_model.set_end_marker(end_marker)

    