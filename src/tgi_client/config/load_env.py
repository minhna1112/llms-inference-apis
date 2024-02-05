import os
from dotenv import load_dotenv


class ENV:
    load_dotenv()
    MODEL_NAME = os.environ.get("TGI_MODEL_NAME", "Phind/Phind-CodeLlama-34B-v2") 
    TGI_HOST = os.environ.get("TGI_HOST", "localhost")
    TGI_PORT = os.environ.get("TGI_PORT", 8001)
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")

env = ENV()