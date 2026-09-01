from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def format_documents(documents):
    """
    Convert retrieved Document objects into a single text context.
    """

    return "\n\n".join(
        document.page_content
        for document in documents
    )


def create_rag_chain(retriever, prompt, llm):

    rag_chain = (
        {
            "context": retriever | format_documents,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain