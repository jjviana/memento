import boto3
import json
bedrock = boto3.client(service_name='bedrock-runtime')

body = json.dumps({
    "prompt": "\n\nHuman:explain black holes to 8th graders\n\nAssistant: Sure, in which language?\n\nHuman: French\n\nAssistant:",
    "max_tokens_to_sample": 8191,
    "temperature": 1.0,
    "top_p": 0.9,
    "stop_sequences": ["explication"]
})

modelId = 'anthropic.claude-v2'
accept = 'application/json'
contentType = 'application/json'

response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

response_body = json.loads(response.get('body').read())
# text
print(response_body)

