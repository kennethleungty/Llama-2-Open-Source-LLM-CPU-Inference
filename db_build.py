# =========================
#  Module: Vector DB Build
# =========================
import yaml
from langchain.vectorstores import FAISS, Milvus
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
import os


# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                   model_kwargs={'device': 'cpu'})


def save_vector_store(filename, loader):
    print(f"Load and split file {str(filename)}")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=cfg['CHUNK_SIZE'],
                                                   chunk_overlap=cfg['CHUNK_OVERLAP'])
    pages = text_splitter.split_documents(documents)

    if cfg['VECTOR_DATABASE'] == "faiss":
        vectorstore = FAISS.from_documents(pages, embeddings)
        vectorstore.save_local(cfg['DB_FAISS_PATH'])
    else:
        vectorstore = Milvus.from_documents(
            pages,
            embeddings,
            collection_name=cfg['MILVUS_COLLECTION_NAME'],
            connection_args={
                "host": cfg['MILVUS_HOSTNAME'], "port": cfg['MILVUS_PORT']},
        )


# Build vector database
def run_db_build():
    # not loading all the files at once because of these errors while I was testing this out: "Odd-length string", "UnicodeEncodeError"
    # loader = DirectoryLoader(cfg['DATA_PATH'],
    #                         glob='*.pdf',
    #                         loader_cls=PyPDFLoader)
    # loader = PyPDFDirectoryLoader(cfg['DATA_PATH'])

    for root, _, files in os.walk(cfg['DATA_PATH']):
        for filename in files:
            # Process the file
            # print(os.path.join(root, filename))
            file = os.path.join(root, filename)
            try:
                if file.endswith(".pdf"):
                    loader = PyPDFLoader(file)
                    save_vector_store(file, loader)
                elif file.endswith(".txt"):
                    loader = TextLoader(file)
                    save_vector_store(file, loader)
                else:
                    continue
            except Exception as e:
                # You can also print the exception message for more information
                print(
                    f"Error on file {str(filename)} message: {str(e)} skipping it and move on to the next")
                continue


if __name__ == "__main__":
    run_db_build()
