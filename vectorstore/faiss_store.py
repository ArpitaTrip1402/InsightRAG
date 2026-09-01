from langchain_community.vectorstores import FAISS


def create_vector_store(chunks, embedding_model):
    """
    Create FAISS vector store from document chunks.
    """

    if not chunks:
        raise ValueError(
            "No document chunks were provided to FAISS."
        )

    if embedding_model is None:
        raise ValueError(
            "Embedding model is not initialized."
        )

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model,
    )

    return vector_store