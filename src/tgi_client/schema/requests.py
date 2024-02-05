from pydantic import BaseModel
from typing import Literal, Optional, List


Role = Literal["system", "user", "assistant"]

class Message(BaseModel):
    role: Role
    content: str

class ModelParams(BaseModel):
    temperature: float = 0
    top_p: float = 1.0
    max_new_tokens: int = 1025
    stream = False

class ModelInputs(BaseModel):
    dialog: List[Message]
    model_params: ModelParams 

class InputRequest(ModelInputs):
    model_name: str = "llama"