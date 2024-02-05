from .code_llama import CodeLLama
from .phind_code_llama import PhinDCodeLlama
from .constants import CODE_LLAMA, PHIND_CODE_LLAMA

import sys
sys.path.extend([".."])
from config.load_env import env

def get_model(
    model_name: str 
):
    if model_name == CODE_LLAMA:
        return CodeLLama(
            model_name=model_name,
            host = env.TGI_HOST,
            port=env.TGI_PORT,
        )
    if model_name== PHIND_CODE_LLAMA:
        return PhinDCodeLlama(
            model_name=model_name,
            host = env.TGI_HOST,
            port=env.TGI_PORT,
        )
    
    