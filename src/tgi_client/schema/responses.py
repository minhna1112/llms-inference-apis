from pydantic import BaseModel
from typing import Literal, Optional, List

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int 

class ChunkResponse(BaseModel):
    id: str
    object: str = ""
    created: int
    model: str
    choices: List[dict]
    
class ChatResponse(ChunkResponse):
    usage: Usage