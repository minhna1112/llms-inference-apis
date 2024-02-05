# llms-inference-apis

Creating inference wrappers for Large Language Models in multiple frameworks: HuggingFace TGI, NVIDIA Triton Inference 

## Requirements:
- Docker, docker-compose
- NVIDIA Container Toolkit
  
## Quickstart

### Run LLM server with your own checkpoints using HuggingFace Text Generation Inference (TGI):
Change `MODEL_NAME` to your HF model code or destination to your checkpoints

```bash
make build_server
```

### Build TGI client:
```bash
make build_client
```

### Run TGI client:
```bash
make run_client
```

## Test the API:
### Using Swagger
1. Open http://localhost:3001 on your browser.
2. Navigate to `/chat_completion` endpoint
3. Try the API by sending requests using the following request body:

```json
{
  "dialog": [
            {
                "role": "system",
                "content": "You are my coding assistant"
            },
            {
                "role": "user",
                "content": "Help me!"
            },
            {
                "role": "assistant",
                "content": "Okay bro!"
            },
            {
                "role": "user",
                "content": "What is Mojo programming?"
            }
  ],
  "model_params": {
    "temperature": 0,
    "top_p": 1,
    "max_gen_len": 1025,
    "stream": false
  },
  "model_name": "codellama/CodeLlama-13b-Instruct-hf"
}
```
### Using Postman
- Send Post request to http://localhost:3001/chat_completion using the previous request body.
- If `stream` is set True, the response will be a stream of server-sent event.