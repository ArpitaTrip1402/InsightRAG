from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    """
    Split loaded documents into smaller chunks.
    """

    if not documents:
        raise ValueError("No documents received for splitting.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
    )

    chunks = splitter.split_documents(documents)

    # Remove empty chunks
    chunks = [
        chunk
        for chunk in chunks
        if chunk.page_content and chunk.page_content.strip()
    ]

    if not chunks:
        raise ValueError(
            "No document chunks were created. "
            "Check PDF loading and text splitting."
        )

    return chunks