# =========================
#  Vector DB Build
#  Author: Kenneth Leung
# =========================
import box
import yaml
from langchain.vectorstores import Chroma, FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

# See for more info: https://huggingface.co/hkunlp/instructor-xl
# EMBED_MODEL = 'hkunlp/instructor-large' # or 'hkunlp/instructor-xl'

# Build vector database
def build_db(vectorstore='FAISS'):
    loader = DirectoryLoader(cfg.DATA_PATH,
                             glob="*.pdf",
                             loader_cls=PyPDFLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=cfg.CHUNK_SIZE,
                                                   chunk_overlap=cfg.CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)
    # embedding = HuggingFaceInstructEmbeddings(model_name=EMBED_MODEL,
    #                                           model_kwargs={"device": 'cuda}
    #                                           )
    # model_name = "sentence-transformers/all-mpnet-base-v2"

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'}

    embeddings = HuggingFaceEmbeddings(model_name=model_name,
                                       model_kwargs=model_kwargs)
    # Build specific DB
    if vectorstore == 'Chroma':
        vectordb = Chroma.from_documents(documents=texts,
                                        embedding=embeddings,
                                        persist_directory=cfg.DB_CHROMA_PATH)
        vectordb.persist()
    elif vectorstore == 'FAISS':
        vectorstore = FAISS.from_documents(texts, embeddings)
        vectorstore.save_local(cfg.DB_FAISS_PATH)
        print('FAISS Vectorstore - Build Complete')
    else:
        raise ValueError('Error in DB selection')

if __name__ == "__main__":
    build_db()
