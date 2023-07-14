from .language_model import LanguageModel,Message
import openai
import datetime
from typing import Callable
import time
    
class GPT_35(LanguageModel):

    def model_name(self) -> str:
        return "gpt-3.5-turbo"

    def __init__(self, api_key: str,logger: Callable = None) -> None:
        openai.api_key = api_key
        self.logger = logger
        self.gc_manager =None
        self.messages = []
        self.end_marker = "{{END}}"
        

    def _logMessage(self, message: Message,total_tokens_used: int):
        if self.logger:
            self.logger(f"{message.tokens_used} / {total_tokens_used} - {message}")

    
    def _log(self,rawMessage: str):
        if self.logger:
            # Write a message preceded by a timestamp in the format YYYY-MM-DD HH:MM:SS
            self.logger(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {rawMessage}\n")
                           
    def initial_prompt(self, prompt: str,need_reply=True) -> str:
        message = Message("user", prompt)
        if need_reply:
            return self._chat_send(message)
        else:
            self.messages.append(message)
            return ""
    
    def _chat_send(self,message: any) -> str:

        messages = self.messages
        if isinstance(message, str):
            messages.append(Message("user", message))
        else:
            messages.append(message)
        
    
        completion = self._completion_with_gc()
            
        response = completion.choices[0].message.content
        finish_reason=completion.choices[0].finish_reason
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        if len(messages)>=2 and messages[-2].tokens_used == 0:
            # Can happen sometimes -  Fill in tokens used now.
            messages[-2].tokens_used = prompt_tokens

        tokens_used_before = sum([m.tokens_used for m in messages])

        messages[-1].tokens_used = prompt_tokens - tokens_used_before


        if finish_reason == "stop":
            response = response + self.end_marker
 
      
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
                    temperature=0.0,
                    stop=self.end_marker)
                if completion.choices[0].finish_reason != "stop":
                    self._log("Max token count exceeded(finish_reason) - Triggering GC")
                    self._gc()
                else:
                    return completion     
            except Exception as e:
                if "maximum context length" in str(e):
                    self._log("Max token count exceeded(exception) - Triggering GC")
                    self._gc()
                elif "You can retry your request" in str(e) or "Rate limit":
                    self._log("Rate limit exceeded - pausing for 5 seconds")
                    time.sleep(5)
                else:
                    raise e
        
        raise Exception("Max token count exceeded - GC failed")
    
    def _gc(self):
        if self.gc_manager:
            self.gc_manager(self)
        else:
            raise Exception("Reached maximum capacity and GC Manager not set")
        
    def _format_messages(self):
        return [m.format() for m in self.messages]
    
    def reset(self):
        self.messages = []

    def get_messages(self) -> list[Message]:
        return self.messages
    
    def set_messages(self,messages:list[Message]):
        self.messages = messages

    def set_gc_manager(self,gc_manager: Callable):
        self.gc_manager = gc_manager

    def set_end_marker(self,end_marker: str):
        self.end_marker = end_marker

               