# Running Open-Source LLMs on CPU Inference for Document Q&A

### Clearly explained step-by-step guide on using C Transformers, GGML, and LangChain for running LLM Python applications on CPU instances

**Step-by-step guide on TowardsDataScience**: *Coming Soon*
___
## Context
- Third-party commercial large language model (LLM) providers like OpenAI's GPT4 have democratized LLM use via simple API calls. 
- However, there are instances where teams would require self-managed or private model deployment for reasons like data privacy and residency rules.
- The proliferation of open-source LLMs has opened up a vast range of options for us, thus reducing our reliance on these third-party providers. 
- When we host open-source LLMs locally on-premise or in the cloud, the dedicated compute capacity becomes a key issue. While GPU instances may seem the obvious choice, the costs can easily skyrocket beyond budget.
- In this project, we will discover how to run quantized versions of open-source LLMs on local CPU inference for document question-and-answer (Q&A).
<br><br>
![Alt text](assets/document_qa_flowchart.png)
___

## Quickstart
- To start passing user queries into the application, launch the terminal from the project directory and run the following command:
`poetry run python main.py "<user query>"`
- For example, `poetry run python main.py "What is the minimum guarantee payable by Adidas?"`
- Note: Omit the prepended `poetry run` if you are NOT using Poetry
<br><br>
![Alt text](assets/qa_output.png)
___
## Tools
- **LangChain**: Framework for developing applications powered by language models
- **C Transformers**: Python bindings for the Transformer models implemented in C/C++ using GGML library
- **FAISS**: Library for efficient similarity search and clustering of dense vectors.
- **Sentence-Transformers (all-MiniLM-L6-v2)**: Pre-trained transformer model for embedding text to a 384 dimensional dense vector space for tasks like clustering or semantic search.
- **MPT-7B-Instruct (LLM)**: Open-source LLM designed for short-form instruction following. It is built by finetuning MPT-7B on a dataset derived from the Databricks Dolly-15k and the Anthropic Helpful and Harmless (HH-RLHF) datasets.
- **Poetry**: Tool for dependency management and Python packaging

___
## Files and Content
- `/assets`: Images relevant to project
- `/config`: Configuration files for LLM application
- `/data`: Dataset used for this project (i.e., Manchester United FC 2022 Annual Report - 177-page PDF document)
- `/models`: Binary file of GGML quantized LLM model (i.e., MPT-7B-Instruct) 
- `/src`: Python codes of key components of LLM application, namely `llm.py`, `utils.py`, and `prompts.py`
- `/vectorstore`: FAISS vector store for documents
- `db_build.py`: Python script to ingest dataset and generate FAISS vector store
- `main.py`: Main Python script to launch the application and to pass user query via command line
- `pyproject.toml`: TOML file to specify which versions of the dependencies used (Poetry)
- `requirements.txt`: List of Python dependencies (and version)
___

## References
- https://github.com/marella/ctransformers
- https://huggingface.co/TheBloke
- https://huggingface.co/TheBloke/MPT-7B-Instruct-GGML
- https://python.langchain.com/en/latest/integrations/ctransformers.html
- https://python.langchain.com/en/latest/modules/models/llms/integrations/ctransformers.html
- https://python.langchain.com/docs/ecosystem/integrations/ctransformers
- https://ggml.ai
- https://github.com/rustformers/llm/blob/main/crates/ggml/README.md
