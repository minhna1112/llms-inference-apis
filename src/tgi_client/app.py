import time
from models import PhinDCodeLlama, CodeLLama
from models.base import BaseChatClient
from typing import Literal, Optional, List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sse_starlette import EventSourceResponse

import os
from common.hashing import hashing

from schema.requests import ModelInputs, InputRequest, ModelParams
from config.config import logger
from config.load_env import ENV
from threading import Thread

from models import get_model

app = FastAPI()


@app.post("/chat_completion")
async def chat_completion(request: InputRequest):
    model_params : ModelParams = request.model_params
    generator = get_model(request.model_name)
    
    if model_params.dict().get("stream") is True:
         response = await llama_chat_completion_stream(generator=generator, model_input=request)
    else:
        response = await llama_chat_completion(generator=generator, model_input=request)    
    return response
    
# @app.post("llama/chat_completion_stream")
async def llama_chat_completion_stream(generator : BaseChatClient, model_input : ModelInputs):
    # model_input = model_input.dict()
    dialogs = [model_input.dialog]
    assert len(dialogs) == 1,  JSONResponse(
        content = "Streaming currently supported for one dialog only",
        status_code = 422
    )
    assert not any([len(dialog) < 1 for dialog in dialogs]), JSONResponse(
        content = "Empty dialog",
        status_code = 422
    )   
    
    message_ids = [hashing() for _ in dialogs]
    model_params = model_input.model_params.dict()
    model_params.update({"request_ids": message_ids})
    model_params.update({"created_time": time.time()})    
    response = EventSourceResponse(generator.chat_completion_stream(
        [[m.dict() for m in dialogs[0]]],  # type: ignore
        **model_params
        ), media_type="text/event-stream")
    # print(response.body_iterator)
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    return response   

# @app.post("llama/chat_completion")
async def llama_chat_completion(generator: BaseChatClient, model_input : ModelInputs):

    dialogs = [model_input.dialog]
    assert not any([len(dialog) < 1 for dialog in dialogs]), JSONResponse(
        content = "Empty dialog",
        status_code = 422
    )
    
    message_ids = [hashing() for _ in dialogs]
    model_params = model_input.model_params.dict()
    model_params.update({"request_ids": message_ids})  
    model_params.update({"created_time": time.time()})
    response =   generator.chat_completion(
        [[m.dict() for m in dialog] for dialog in dialogs],  # type: ignore
        **model_params
        )

    return response        


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
