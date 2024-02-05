from typing import Dict, List, Optional

from text_generation.types import Response

from models.base import Dialog, Message
from schema.responses import ChatResponse, ChunkResponse, Usage
from models.base import BaseChatClient
from models.constants import CODE_LLAMA, COMPLETION_CHUNK, COMPLETION_MESSAGE, MESSAGE_ID_PREFIX, STOP
from models.base import Dialog
from schema.responses import ChatResponse
from models.phind_code_llama import PhinDCodeLlama
from models.base import Dialog, Message

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

SPECIAL_TAGS = [B_INST, E_INST, "<<SYS>>", "<</SYS>>"]
UNSAFE_ERROR = "Error: special tags are not allowed as part of the prompt."

class CodeLLama(PhinDCodeLlama):
    def __init__(self, model_name: str = ..., host: str = "localhost", port: int = 8080, url: Optional[str]  = None, headers: Optional[Dict[str, str]]  = None, cookies: Optional[Dict[str, str]]  = None, timeout: int = 10):
        super().__init__(model_name, host, port, url, headers, cookies, timeout)
        self.model_name = CODE_LLAMA
    
    def preprocess(self, dialogs: List[Dialog]):
        dialog = dialogs[0]
        unsafe_requests = []
        unsafe_requests.append(
                any([tag in msg["content"] for tag in SPECIAL_TAGS for msg in dialog])
            )
        if dialog[0]["role"] == "system":
            dialog = [
                {
                    "role": dialog[1]["role"],
                    "content": B_SYS
                    + dialog[0]["content"]
                    + E_SYS
                    + dialog[1]["content"],
                }
            ] + dialog[2:]
        assert all([msg["role"] == "user" for msg in dialog[::2]]) and all(
            [msg["role"] == "assistant" for msg in dialog[1::2]]
        ), (
            "model only supports 'system', 'user' and 'assistant' roles, "
            "starting with 'system', then 'user' and alternating (u/a/u/a/u...)"
        )
        dialog_strings: List[str] = [
                
                f"{B_INST} {(prompt['content']).strip()} {E_INST} {(answer['content']).strip()} "
                
                for prompt, answer in zip(
                    dialog[::2],
                    dialog[1::2],
                )
            ]
        assert (
            dialog[-1]["role"] == "user"
        ), f"Last message must be from user, got {dialog[-1]['role']}"
        
        dialog_strings.append(f"{B_INST} {(dialog[-1]['content']).strip()} {E_INST}"),
        return " ".join(dialog_strings)

if __name__=="__main__":
    
    client = CodeLLama(
        host="4.193.50.237",
        port=8001
    )
    
    # out = client.chat_completion(dialogs=[
    #         [
    #             Message(role="system", content="You are coding assistant named codeVista"),
    #             Message(role="user", content= "generate Djikstra Algorithm in Python")
    #         ]
    #     ],
    #     max_new_tokens = 128,
    #     stream=False,
    #     message_id = "0",
    #     created_time = 0)
    
    # print(out)
    
    for a in  client.chat_completion_stream(
        [
            [
                Message(role="system", content="You are coding assistant named codeVista"),
                Message(role="user", content= "generate Djikstra Algorithm in Python")
            ]
        ],
        max_new_tokens = 128,
        stream=True,
        message_id = "0",
        created_time = 0
    ):
        print(a)