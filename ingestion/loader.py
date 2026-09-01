from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path: str):
    """
    Load text from a PDF file.

    Returns:
        list: LangChain Document objects
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    loader = PyPDFLoader(str(path))
    documents = loader.load()

    if not documents:
        raise ValueError(
            "PDF was loaded, but no pages were extracted. "
            "The PDF may be scanned/image-based or corrupted."
        )

    # Remove completely empty pages
    documents = [
        doc for doc in documents
        if doc.page_content and doc.page_content.strip()
    ]

    if not documents:
        raise ValueError(
            "PDF contains no extractable text. "
            "If this is a scanned PDF, OCR is required."
        )

    return documents