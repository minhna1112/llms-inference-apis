from typing import Dict, Optional, TypedDict, List, Literal
from text_generation import Client, AsyncClient
from schema.responses import ChatResponse

Role = Literal["system", "user", "assistant"]


class Message(TypedDict):
    role: Role
    content: str


Dialog = List[Message]


class BaseChatClient(Client):
    def __init__(self, 
                 model_name: str,
                 host: str,
                 port: int, 
                 url: Optional[str],
                 headers: Optional[Dict[str, str]]  = None, 
                 cookies: Optional[Dict[str, str]]  = None, 
                 timeout: int = 10):
        self.model_name = model_name
        base_url = f'http://{host}:{str(port)}' if not url else url
        super().__init__(base_url, headers, cookies, timeout)
        
    def chat_completion(self, dialogs: List[Dialog], **kwargs)->ChatResponse:
        raise NotImplemented
    
    def chat_completion_stream(self, dialogs: List[Dialog], **kwargs)->ChatResponse:
        raise NotImplemented
    
    
class BaseAsyncChatClient(AsyncClient):
    def __init__(self, 
                 model_name: str,
                 host: str,
                 port: int, 
                 url: Optional[str],
                 headers: Optional[Dict[str, str]]  = None, 
                 cookies: Optional[Dict[str, str]]  = None, 
                 timeout: int = 10):
        self.model_name = model_name
        base_url = f'http://{host}:{str(port)}' if not url else url
        super().__init__(base_url, headers, cookies, timeout)
        
    async def chat_completion(self, dialogs: List[Dialog], **kwargs)->ChatResponse:
        raise NotImplemented
    
    async def chat_completion_stream(self, dialogs: List[Dialog], **kwargs)->ChatResponse:
        raise NotImplemented
    