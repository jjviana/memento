import json
import pprint
from dataclasses import dataclass
from typing import List

from lark import Lark, Transformer, Discard

grammar = '''
    %import common.WS
    start:  embedded_message*
    embedded_message: anything_before message anything_after
    message: "{{FROM:" WS? entity_id WS "TO:" WS? entity_id WS? "}}" content "{{END}}"
    anything_before: /./s*
    anything_after: /./s*
    content: /./s*
    entity_id: /[A-Za-z0-9]+/

'''

@dataclass
class Message:
    """"
    A message from one entity to another
    """
    msg_from: str
    msg_to: str
    msg_content: str

@dataclass
class EmbeddedMessage:
    """"
    A message potentially embedded in other text
    """
    before_content: str
    message: Message
    after_content: str


class MessageTransformer(Transformer):
    def start(self,args):
        return args
    def embedded_message(self, args):
        before_content = None
        message = None
        after_content = None
        if len(args) > 1:
            before_content = args[0]
            message = args[1]
        if len(args) > 2:
            after_content = args[2]

        return EmbeddedMessage(before_content, message, after_content)


    def message(self, args):
        args = [arg for arg in args if arg is not Discard]
        return Message(args[0], args[1], args[2])

    def entity_id(self, args):
        return str(args[0])

    def anything_before(self, args):
        return ''.join(str(arg) for arg in args)

    def anything_after(self, args):
        return ''.join(str(arg) for arg in args)

    def content(self, args):
        return ''.join(str(arg) for arg in args)

    def WS(self, args):
        return Discard


parser = Lark(grammar, parser='lalr', transformer=MessageTransformer())


def parse_message(message) -> List[EmbeddedMessage]:
    return parser.parse(message)





