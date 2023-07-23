'''
===========================================
        Module: Util functions
===========================================
'''
import yaml

from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS, Milvus
from src.prompts import qa_template
from src.llm import build_llm

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = yaml.safe_load(ymlfile)


def set_qa_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=qa_template,
                            input_variables=['context', 'question'])
    return prompt


def build_retrieval_qa(llm, prompt, vectordb):
    dbqa = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=vectordb.as_retriever(
                                           search_kwargs={'k': cfg['VECTOR_COUNT']}),
                                       return_source_documents=cfg['RETURN_SOURCE_DOCUMENTS'],
                                       chain_type_kwargs={'prompt': prompt}
                                       )
    return dbqa


def setup_dbqa():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})

    if cfg['VECTOR_DATABASE'] == "faiss":
        vectordb = FAISS.load_local(cfg['DB_FAISS_PATH'], embeddings)
    else:
        vectordb: Milvus = Milvus(
            embedding_function=embeddings,
            collection_name=cfg['MILVUS_COLLECTION_NAME'],
            connection_args={
                "host": cfg['MILVUS_HOSTNAME'], "port": cfg['MILVUS_PORT']},
        )

    llm = build_llm()
    qa_prompt = set_qa_prompt()
    dbqa = build_retrieval_qa(llm, qa_prompt, vectordb)

    return dbqa
