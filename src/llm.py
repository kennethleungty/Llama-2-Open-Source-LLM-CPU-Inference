'''
===========================================
        Module: Open-source LLM Setup
===========================================
'''
from langchain.llms import CTransformers
import yaml

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = yaml.safe_load(ymlfile)


def build_llm():
    # Local CTransformers model
    llm = CTransformers(model=cfg['MODEL_BIN_PATH'],
                        model_type=cfg['MODEL_TYPE'],
                        config={'max_new_tokens': cfg['MAX_NEW_TOKENS'],
                                'temperature': cfg['TEMPERATURE']}
                        )

    return llm
