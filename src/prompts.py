'''
===========================================
        Module: Prompts collection
===========================================
'''
# Note that the spacing and indentation of the prompt template is important for MPT-7B-Instruct, as it is highly sensitive to these
# whitespace changes. For example, it could have problems generating a summary from the pieces of context

qa_template = """You are an expert HR assistant. Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Question: {question}

Helpful detailed answer:"""
