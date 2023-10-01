from typing import Callable

import boto3
import json
from .language_model import LanguageModel, Message


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

        body = json.dumps({
            "prompt": self.format_prompt(),
            "max_tokens_to_sample": 8191,
            "temperature": 1.0,
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
        completion = completion + self.end_marker
        self.messages.append(Message("assistant", completion))
        self._log_message(messages[-2])
        self._log_message(messages[-1])
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


    def _log_message(self, message: Message):
        if self.logger:
            self.logger(f"{message}")

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
