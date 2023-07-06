import box
import yaml
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate)
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from src.prompts import mpt_7b_qa_template

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def set_qa_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    # messages = [
    #     SystemMessagePromptTemplate.from_template(qa_system_template_prefix),
    #     SystemMessagePromptTemplate.from_template(qa_system_template_main),
    #     HumanMessagePromptTemplate.from_template('{question}')
    #     ]
    # qa_prompt = ChatPromptTemplate.from_messages(messages)

    prompt = PromptTemplate(template=mpt_7b_qa_template,
                            input_variables=['context', 'question'])
    return prompt


def build_retrieval_qa(llm, prompt, vectordb):
    dbqa = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=vectordb.as_retriever(search_kwargs={'k': cfg.VECTOR_COUNT}),
                                       return_source_documents=cfg.RETURN_SOURCE_DOCUMENTS,
                                       chain_type_kwargs={'prompt': prompt}
                                       )
    return dbqa
