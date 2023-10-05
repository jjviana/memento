from protocol import parse_message,EmbeddedMessage
import unittest

class TestMessage(unittest.TestCase):
    def test_parse_message(self):
        message1 = "Hello there!Message for you:\n{{FROM:entity1 TO: xntity2}}Some content here{{END}}Bye."
        result1 = parse_message(message1)
        print(result1)
        assert len(result1) == 1
        assert result1[0].before_content == "Hello there!Message for you:\n"
        assert result1[0].message.msg_from == "entity1"
        assert result1[0].message.msg_to == "xntity2"
        assert result1[0].message.msg_content == "Some content here"
        assert result1[0].after_content == "Bye."

        message2 = message1+"\nHello again!Nice to meet you, here is a message:\n{{FROM:entity1 TO: entity2}}Some more \ncontent here{{END}}Bye for reals!"
        result2 = parse_message(message2)
        print(result2)
        assert len(result2) == 2
        assert result2[0].before_content == "Hello there!Message for you:\n"
        assert result2[0].message.msg_from == "entity1"
        assert result2[0].message.msg_to == "xntity2"
        assert result2[0].message.msg_content == "Some content here"
        assert result2[0].after_content == "Bye.\nHello again!Nice to meet you, here is a message:\n"
        assert result2[1].before_content == ""
        assert result2[1].message.msg_from == "entity1"
        assert result2[1].message.msg_to == "entity2"
        assert result2[1].message.msg_content == "Some more \ncontent here"
        assert result2[1].after_content == "Bye for reals!"

        message3 = "{{FROM:entity1 TO: entity2}}🤨{{END}}"
        result3 = parse_message(message3)
        print(result3)
        assert len(result3) == 1
        assert result3[0].before_content == ""
        assert result3[0].message.msg_from == "entity1"
        assert result3[0].message.msg_to == "entity2"
        assert result3[0].message.msg_content == "🤨"
        assert result3[0].after_content == ""

        exception = False 
        try:
            message4 = "No content here"
            result4 = parse_message(message4)
        except Exception as e:
            exception = True
        
        assert exception


    