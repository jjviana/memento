import os
from typing import Callable

import boto3
import json
from .language_model import LanguageModel, Message
import tokenizers


# A LLM implementation on top of Amazon Bedrock using the Claude model
class BedrockClaude(LanguageModel):

    def __init__(self, model_id: str, logger: Callable = None):
        self.model_id = model_id
        self.messages = []
        self.end_marker = "{{END}}"
        self.bedrock = boto3.client(service_name='bedrock-runtime')
        self.accept = 'application/json'
        self.content_type = 'application/json'
        self.logger = logger
        self.gc_manager = None

        # Load the tokenizer from the file claude_tokenizer.json that is located in the
        # same directory as this file
        dir = os.path.dirname(__file__)
        tokenizer_file = os.path.join(dir, 'claude_tokenizer.json')
        self.tokenizer = tokenizers.Tokenizer.from_file(tokenizer_file)
        
    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text).ids)

    def initial_prompt(self, prompt: str, need_reply=True) -> str:
        message = Message("user", prompt)
        if need_reply:
            return self._chat_send(message)
        else:
            self.messages.append(message)
            return ""

    def _chat_send(self, message: Message) -> str:
        messages = self.messages
        if isinstance(message, str):
            messages.append(Message("user", message))
        else:
            messages.append(message)

        prompt = self.format_prompt()
        promot_token_count = self.count_tokens(prompt)
        body = json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 8191,
            "temperature": 0.5,
            "top_p": 0.9,
            "stop_sequences": [self.end_marker]
        })

        response = self.bedrock.invoke_model(body=body, modelId=self.model_id, accept=self.accept,
                                             contentType=self.content_type)
        response_body = json.loads(response.get('body').read())
        completion = response_body['completion']
        stop_reason = response_body['stop_reason']
        if stop_reason != "stop_sequence":
            raise Exception(f"Unexpected model stop reason: {stop_reason}")
        completion_token_count = self.count_tokens(completion)
        completion = completion + self.end_marker

        if len(messages)>=2 and messages[-2].tokens_used == 0:
            # Can happen sometimes -  Fill in tokens used now.
            messages[-2].tokens_used = promot_token_count

        tokens_used_before = sum([m.tokens_used for m in messages])
        self.messages[-1].tokens_used = promot_token_count - tokens_used_before

        response_message = Message("assistant", completion)
        response_message.tokens_used = completion_token_count
        response_message.total_prompt_tokens = promot_token_count
        response_message.total_completion_tokens = completion_token_count
        response_message.cost = self.compute_cost(promot_token_count,completion_token_count)
        self.messages.append(response_message)

        total_tokens_used = promot_token_count + completion_token_count

        self._logMessage(messages[-2],total_tokens_used)
        self._logMessage(messages[-1],total_tokens_used)
        return completion

    def format_prompt(self) -> str:
        prompt=""
        for message in self.messages:
            if message.role=="user":
                prompt+=f"\n\nHuman: {message.content}"
            elif message.role=="assistant":
                prompt+=f"\n\nAssistant: {message.content}"
            else:
                raise Exception(f"Unexpected message role: {message.role}")
        prompt+="\n\nAssistant:"
        return prompt


    def _logMessage(self, message: Message,total_tokens_used: int):

        # format message cost with 6 digits
        cost = "{:.6f}".format(message.cost)
        if self.logger:
            self.logger(f"{message.tokens_used} / {total_tokens_used}- {cost} - {message}")


    def compute_cost(self,prompt_tokens,completion_tokens):
        prompt_tokens_float = float(prompt_tokens)/1000.0
        completion_tokens_float = float(completion_tokens)/1000.0

        return prompt_tokens_float*0.01102+completion_tokens_float*0.03268
       
        
    def input(self, prompt: str) -> str:
        return self._chat_send(prompt)

    def reset(self):
        self.messages = []

    def get_messages(self) -> list[Message]:
        return self.messages

    def set_messages(self, messages: list[Message]):
        self.messages = messages

    def set_gc_manager(self, gc_manager: Callable):
        pass

    def set_end_marker(self, end_marker: str):
        self.end_marker = end_marker
