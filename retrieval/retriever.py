from config import TOP_K


def get_retriever(vectorstore):
    """
    Convert the vector store into a LangChain retriever.
    """

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": TOP_K
        }
    )

    return retriever