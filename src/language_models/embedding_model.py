
from abc import abstractmethod
from tenacity import retry, wait_random_exponential, stop_after_attempt
import openai


class EmbeddingModel:
    @abstractmethod
    def embed(self,text:str) -> list:
        pass


class OpenAIEmbeddingModel(EmbeddingModel):
    def __init__(self,openai_api_key) -> None:
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        
    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def embed(self,text:str) -> list:
        return  openai.Embedding.create(
    input=text, model="text-embedding-ada-002")["data"][0]["embedding"]
    