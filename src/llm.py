from langchain import SagemakerEndpoint
from langchain.llms import HuggingFacePipeline, GPT4All, CTransformers
from langchain.llms.sagemaker_endpoint import LLMContentHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from dotenv import find_dotenv, load_dotenv
from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline
from typing import Dict


import box
import json
import torch
import os
import yaml

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def build_llm():
    # Local CTransformers MPT-7B-Instruct
    llm = CTransformers(model=cfg.MODEL_BIN_PATH,
                        model_type=cfg.MODEL_TYPE,
                        config={'max_new_tokens': cfg.MAX_NEW_TOKENS,
                                'temperature': cfg.TEMPERATURE}
                        )

    # # HuggingFace Models
    # tokenizer = LlamaTokenizer.from_pretrained("TheBloke/wizardLM-7B-HF")
    # model = LlamaForCausalLM.from_pretrained("TheBloke/wizardLM-7B-HF",
    #                                             load_in_8bit=True,
    #                                             device_map='auto',
    #                                             # torch_dtype=torch.float16,
    #                                             low_cpu_mem_usage=True
    #                                             )
    # pipe = pipeline(
    #     "text-generation",
    #     model=model,
    #     tokenizer=tokenizer,
    #     max_length=1024,
    #     temperature=0,
    #     top_p=0.95,
    #     repetition_penalty=1.15
    # )
    # llm = HuggingFacePipeline(pipeline=pipe)

    # # OpenAI API
    # llm = ChatOpenAI(
    #                 model_name='gpt-3.5-turbo',
    #                 temperature=0,
    #                 openai_api_key=os.environ['OPENAI_API_KEY'],
    #                 max_tokens=256
    #                )

    # # Local GPT4ALL
    # model_path = 'bin/ggml-gpt4all-j-v1.3-groovy.bin'
    # # callbacks = [StreamingStdOutCallbackHandler()]
    # llm = GPT4All(model=model_path,
    #             #   backend='gptj',
    #             #   callbacks=callbacks,
    #               verbose=True)

    # # AWS SageMaker endpoint
    # class ContentHandler(LLMContentHandler):
    #     content_type = "application/json"
    #     accepts = "application/json"

    #     def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
    #         input_str = json.dumps({prompt: prompt, **model_kwargs})
    #         return input_str.encode('utf-8')

    #     def transform_output(self, output: bytes) -> str:
    #         response_json = json.loads(output.read().decode("utf-8"))
    #         return response_json[0]["generated_text"]

    # content_handler = ContentHandler()

    # llm = SagemakerEndpoint(
    #         endpoint_name=cfg.AWS_SAGEMAKER_ENDPOINT_NAME,
    # #         credentials_profile_name="credentials-profile-name",
    #         region_name=cfg.AWS_REGION,
    #         model_kwargs={"temperature":1e-10},
    #         content_handler=content_handler)

    return llm
