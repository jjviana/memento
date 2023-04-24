from .language_model import LanguageModel
import openai
import datetime
from typing import Callable

class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
        self.tokens_used = 0

    def __str__(self):
        return f"{self.role}: {self.content}"

    def __repr__(self):
        return str(self)
    
    def format(self):
        return {
            "role": self.role,
            "content": self.content
        }
    
class GPT_35(LanguageModel):

    def model_name(self) -> str:
        return "gpt-3.5-turbo"

    def __init__(self, api_key: str,logger: Callable = None):
        openai.api_key = api_key
        self.logger = logger
        self.messages = []

    def _logMessage(self, message: str,total_tokens_used: int):
        if self.logger:
            self.logger(f"{message.tokens_used} / {total_tokens_used} - {message}")

    
    def _log(self,rawMessage: str):
        if self.logger:
            # Write a message preceded by a timestamp in the format YYYY-MM-DD HH:MM:SS
            self.logger(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {rawMessage}\n")
            

                              
            
                    
    def initial_prompt(self, prompt: str) -> str:

        message = Message("system", prompt)
        return self._chat_send(message)
    
    def _chat_send(self,message: any) -> str:

        messages = self.messages
        if isinstance(message, str):
            messages.append(Message("user", message))
        else:
            messages.append(message)
        
        
        tokens_used_before = sum([m.tokens_used for m in messages])
        
        completion = self._completion_with_gc()
            
        response = completion.choices[0].message.content
        finish_reason=completion.choices[0].finish_reason
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        messages[-1].tokens_used = prompt_tokens - tokens_used_before
        if finish_reason == "stop":
            response = response + "{{END}}"
 
      
        response_message = Message("assistant", response)
        response_message.tokens_used = completion_tokens
        messages.append(response_message)
        total_tokens_used = prompt_tokens + completion_tokens
        self._logMessage(messages[-2],total_tokens_used)
        self._logMessage(messages[-1],total_tokens_used)
        self.messages = messages
        return response

    def input(self, prompt: str) -> str:
        return self._chat_send(prompt)

    def _completion_with_gc(self) -> any:
        for i in range (0, 10):
            try:
                completion = openai.ChatCompletion.create(
                    model=self.model_name(),
                    messages=self._format_messages(),
                    temperature=0,
                    stop="{{END}}")
                if completion.choices[0].finish_reason != "stop":
                    self._log("Max token count exceeded(finish_reason) - Triggering GC")
                    self._gc()
                else:
                    return completion     
            except Exception as e:
                if "maximum context length" in str(e):
                    self._log("Max token count exceeded(exception) - Triggering GC")
                    self._gc()
                else:
                    raise e
        
        raise Exception("Max token count exceeded - GC failed")
    
    def _gc(self):
        # By default we remove the oldest non-system messages until
        # we have freed at least 400 tokens

        new_messages = []
        tokens_freed = 0
        for message in self.messages:
            if message.role != "system":
                if tokens_freed < 400:
                    tokens_freed += message.tokens_used
                else:
                    new_messages.append(message)
            else:
                new_messages.append(message)

        self._log(f"GC - Freed {tokens_freed} tokens")
        self.messages = new_messages
        
    def _format_messages(self):
        return [m.format() for m in self.messages]


               