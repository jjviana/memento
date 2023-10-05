import json
import pprint
from dataclasses import dataclass

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
    msg_from: str
    msg_to: str
    msg_content: str

@dataclass
class EmbeddedMessage:
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


def parse_message(message):
    return parser.parse(message)


message1 = "Hello there!Message for you:\n{{FROM:entity1 TO: xntity2}}Some content here{{END}}Bye."
result1 = parse_message(message1)
print(result1)

message2 = message1+"\nHello again!Nice to meet you, here is a message:\n{{FROM:entity1 TO: entity2}}Some more \ncontent here{{END}}Bye for reals!"
result2 = parse_message(message2)
print(result2)

message3 = "{{FROM:entity1 TO: entity2}}    \n🤨{{END}}"
result3 = parse_message(message3)
print(result3)


