from typing import Dict, List, Optional

from text_generation.types import Response

from models.base import Dialog, Message
from schema.responses import ChatResponse, ChunkResponse, Usage
from models.base import BaseChatClient
from models.constants import PHIND_CODE_LLAMA, COMPLETION_CHUNK, COMPLETION_MESSAGE, MESSAGE_ID_PREFIX, STOP
from models.base import Dialog
from schema.responses import ChatResponse

USER_PREFIX = "### User Message\n"
SYSTEM_PREFIX = "### System Prompt\n"
ASSISTANT_PREFIX = "### Assistant\n"

class PhinDCodeLlama(BaseChatClient):
    def __init__(self,
                 model_name: str =  PHIND_CODE_LLAMA, 
                 host: str = "localhost", 
                 port: int = 8080,
                 url: Optional[str] = None,
                 headers: Optional[Dict[str, str]]  = None, 
                 cookies: Optional[Dict[str, str]]  = None, 
                 timeout: int = 10):
        self.model_name = model_name
        super().__init__(model_name, host, port, url, headers, cookies, timeout)    

    def msg2prompt(self, msg: Message):
            content = msg["content"].replace("\n", " ")
            if msg["role"] in ["user"]:
                return USER_PREFIX + content
            if msg["role"] in ["system"]:
                return SYSTEM_PREFIX + content
            if msg["role"] in ["assistant"]:
                return ASSISTANT_PREFIX + content    

    def preprocess(self, dialogs: List[Dialog] ):

        
        input_text  = "\n\n".join([
                    self.msg2prompt(msg)                     
                    for msg in dialogs[-1]
                ])
        
        
        
        # inputs.pop("token_type_ids")
        return input_text

    def chat_completion_stream(self, dialogs: List[Dialog], **kwargs) -> ChunkResponse:
        input_text = self.preprocess(dialogs=dialogs)
        print(input_text)
        request_id = MESSAGE_ID_PREFIX + kwargs.get("request_ids")[0]
        created_time  = int(kwargs.get("created_time"))
        for chunk in self.generate_stream(prompt=input_text, max_new_tokens=kwargs.get("max_new_tokens")):

            choice = {
                "message_id": request_id,
                "index": 0,
                "delta": str(chunk.token.text),
                "finish": None
            }
            chat_response =  ChunkResponse(**{
                "id": request_id,
                "object": str(COMPLETION_CHUNK),
                "created": created_time,
                "model": self.model_name,
                "choices": [choice]
            })
            yield  chat_response

    
    def chat_completion(self, dialogs: List[Dialog], **kwargs) -> ChatResponse:
        input_text = self.preprocess(dialogs=dialogs)        
        
        request_id = MESSAGE_ID_PREFIX + kwargs.get("request_ids")[0]
        created_time  = int(kwargs.get("created_time"))
 
        response = self.generate(
            prompt= input_text,
            max_new_tokens= kwargs.get("max_new_tokens")
            
        )
        print(response)
        details = response.details
        usage = Usage(
            prompt_tokens= len(input_text),
            completion_tokens=response.details.generated_tokens,
            total_tokens= len(input_text) + response.details.generated_tokens
        )
        choice  = {
            "index" : 0,
            "message": Message(
                role = 'assistant',
                content = response.generated_text
            ),
            "finish_reason": STOP
        }
        return ChatResponse(
                id = request_id,
                object=COMPLETION_MESSAGE,
                created= created_time,
                model=self.model_name,
                choices= [choice],
                usage= usage
            )
        
        
            
        
        
if __name__=="__main__":
    client = PhinDCodeLlama(
        host="4.193.50.237",
        port=8001
    )
    
    result =  client.chat_completion(
        [
            [
                Message(role="user", content= "generate Djikstra Algorithm in Python")
            ]
        ],
        max_new_tokens = 128,
        stream=False,
        message_id = "0",
        created_time = 0
    )
    
    print(result)
    
    for a in  client.chat_completion_stream(
        [
            [
                Message(role="user", content= "generate Djikstra Algorithm in Python")
            ]
        ],
        max_new_tokens = 128,
        stream=True,
        message_id = "0",
        created_time = 0
    ):
        print(a)