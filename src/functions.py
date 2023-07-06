import box
import yaml
from dotenv import find_dotenv, load_dotenv
from langchain.vectorstores import Chroma, FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from src.utils import set_qa_prompt, build_retrieval_qa
from src.llm import build_llm

load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def setup_dbqa():
    # embedding = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl",
    #                                           model_kwargs={"device": "cpu"})
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})

    if cfg.DB_TYPE == 'Chroma':
        vectordb = Chroma(persist_directory=cfg.DB_CHROMA_PATH,
                          embedding_function=embeddings)
    elif cfg.DB_TYPE == 'FAISS':
        vectordb = FAISS.load_local(cfg.DB_FAISS_PATH, embeddings)
    else:
        raise Exception('Error in vectorstore selection')

    llm = build_llm()
    qa_prompt = set_qa_prompt()
    dbqa = build_retrieval_qa(llm, qa_prompt, vectordb)

    return dbqa
