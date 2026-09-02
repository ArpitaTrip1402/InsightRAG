# 🔎 InsightRAG — RAG-Based Document Research System

> **Ask questions about your documents and get context-grounded answers.**

**InsightRAG** is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their content.

The system combines **LangChain, Gemini, embeddings, FAISS vector search, retrieval/reranking, and Streamlit** to retrieve relevant information from uploaded documents and use that context to generate relevant answers.

### 🚀 Live Demo

**[Open InsightRAG](https://insightrag-h63dbddz4q3ytqfyevspid.streamlit.app/)**

---

## ✨ Features

* 📄 **PDF Document Upload** — Upload PDF documents directly through the application.
* 📖 **PDF Text Extraction** — Extracts textual content from uploaded documents.
* ✂️ **Intelligent Text Chunking** — Splits documents into smaller chunks for effective retrieval.
* 🧠 **Embeddings** — Converts document chunks into vector representations.
* 🔎 **FAISS Vector Search** — Retrieves relevant document chunks using semantic similarity.
* 🎯 **Context Retrieval & Reranking** — Selects relevant context before generation.
* 🤖 **Gemini-Powered Generation** — Uses Google's Gemini API to generate responses from retrieved context.
* 🖥️ **Interactive Streamlit UI** — Provides a simple interface for document upload and question answering.
* 🔐 **Secure API Configuration** — API keys are managed through environment variables or Streamlit Secrets.
* ☁️ **Cloud Deployment** — Deployed using Streamlit Community Cloud.

---

# 🏗️ System Architecture

InsightRAG follows a modular RAG pipeline:

```text
                         ┌─────────────────────┐
                         │     Streamlit UI    │
                         │       app.py        │
                         └──────────┬──────────┘
                                    │
                         Upload PDF / Ask Query
                                    │
                    ┌───────────────▼───────────────┐
                    │          INGESTION             │
                    │                                │
                    │  loader.py → splitter.py      │
                    │                                │
                    │ PDF → Documents → Chunks       │
                    └───────────────┬────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │          EMBEDDINGS             │
                    │                                │
                    │        embedder.py             │
                    │                                │
                    │  Documents → Vector Embeddings │
                    └───────────────┬────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │         VECTOR STORE            │
                    │                                │
                    │       faiss_store.py           │
                    │            FAISS               │
                    └───────────────┬────────────────┘
                                    │
                                    │
                              User Query
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │          RETRIEVAL              │
                    │                                │
                    │       retriever.py             │
                    │          ↓                     │
                    │       reranker.py              │
                    │                                │
                    │  Relevant Context Selection    │
                    └───────────────┬────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │          GENERATION             │
                    │                                │
                    │       prompt.py                │
                    │          ↓                     │
                    │     rag_chain.py               │
                    │          ↓                     │
                    │        llm.py                  │
                    │          ↓                     │
                    │        Gemini                  │
                    └───────────────┬────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Final Answer     │
                         └─────────────────────┘
```

---

# 🔄 RAG Pipeline

The complete workflow is:

```text
PDF Upload
     ↓
PDF Loading
     ↓
Text Extraction
     ↓
Text Splitting
     ↓
Document Chunks
     ↓
Embedding Generation
     ↓
FAISS Vector Store
     ↓
User Question
     ↓
Similarity Retrieval
     ↓
Reranking
     ↓
Relevant Context
     ↓
Prompt Construction
     ↓
Gemini LLM
     ↓
Context-Grounded Answer
```

### 1. Document Ingestion

The user uploads a PDF through the Streamlit interface.

The PDF loader extracts the available textual content and converts it into documents that can be processed by the RAG pipeline.

### 2. Text Splitting

Large documents are divided into smaller overlapping chunks.

Chunking allows the retrieval system to search for relevant sections instead of passing the entire document to the language model.

### 3. Embedding Generation

Each document chunk is converted into a vector representation using the configured embedding model.

These vectors capture semantic relationships between pieces of text.

### 4. FAISS Vector Store

The generated embeddings are stored in a **FAISS vector index**.

FAISS enables similarity-based retrieval of document chunks that are semantically relevant to the user's question.

### 5. Retrieval

When the user asks a question, the query is converted into an embedding and compared against the stored document vectors.

```text
User Question
      ↓
Query Embedding
      ↓
FAISS Similarity Search
      ↓
Relevant Chunks
```

### 6. Reranking

Retrieved results can be processed through the reranking layer to improve the relevance of the context selected for generation.

### 7. Prompt Construction

The retrieved context is combined with the user's question through the RAG prompt.

```text
Retrieved Context + User Question
                ↓
           RAG Prompt
```

### 8. Gemini Generation

The prepared prompt is sent to the Gemini model.

The model generates the final response using the retrieved document context.

```text
Question + Context
       ↓
     Gemini
       ↓
 Final Answer
```

---

# 🧩 Project Structure

```text
InsightRAG/
│
├── app.py                         # Streamlit application / UI
├── config.py                      # Application configuration
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── .gitignore                     # Git ignored files
│
├── ingestion/                     # PDF processing
│   ├── loader.py                  # PDF document loading
│   ├── splitter.py                # Text chunking
│   └── __init__.py
│
├── embeddings/                    # Embedding generation
│   ├── embedder.py                # Embedding model
│   └── __init__.py
│
├── vectorstore/                   # Vector store layer
│   ├── faiss_store.py             # FAISS vector store creation
│   └── __init__.py
│
├── retrieval/                     # Retrieval pipeline
│   ├── retriever.py               # Similarity retrieval
│   ├── reranker.py                # Context reranking
│   └── __init__.py
│
├── generation/                    # LLM generation
│   ├── llm.py                     # Gemini configuration
│   ├── prompt.py                  # RAG prompt
│   ├── rag_chain.py               # RAG pipeline
│   └── __init__.py
│
└── data/                          # Local data storage
    ├── uploads/                   # Uploaded PDF files
    └── vectorstore/               # Local vector-store data
```

---

# 📦 Module Responsibilities

| Module                       | Responsibility                               |
| ---------------------------- | -------------------------------------------- |
| `app.py`                     | Streamlit interface and application workflow |
| `config.py`                  | Application configuration                    |
| `ingestion/loader.py`        | Loads and extracts PDF content               |
| `ingestion/splitter.py`      | Splits documents into chunks                 |
| `embeddings/embedder.py`     | Generates document embeddings                |
| `vectorstore/faiss_store.py` | Creates the FAISS vector store               |
| `retrieval/retriever.py`     | Retrieves relevant document chunks           |
| `retrieval/reranker.py`      | Reranks retrieved context                    |
| `generation/prompt.py`       | Defines the RAG prompt                       |
| `generation/llm.py`          | Configures the Gemini model                  |
| `generation/rag_chain.py`    | Connects retrieval and generation            |

---

# 🛠️ Tech Stack

### Generative AI

* **Google Gemini API**
* **LangChain**
* **Retrieval-Augmented Generation (RAG)**

### Document Processing

* **PyPDF**
* LangChain document processing
* Recursive text splitting

### Vector Search

* **FAISS**
* Semantic embeddings
* Similarity retrieval

### Application

* **Python**
* **Streamlit**

### Deployment

* **Streamlit Community Cloud**

### Development

* Git
* GitHub
* Python virtual environment

---

# 🚀 Getting Started

## Prerequisites

Make sure you have:

* Python 3.11+
* Git
* A Google Gemini API key

---

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/InsightRAG.git
cd InsightRAG
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 API Configuration

InsightRAG uses the **Google Gemini API** for response generation.

For local development, create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

### Important

Never commit your API key to GitHub.

Your `.gitignore` should include:

```gitignore
.env
.venv/
__pycache__/
*.pyc
data/uploads/
data/vectorstore/
```

---

# ▶️ Run the Application

Start Streamlit with:

```bash
streamlit run app.py
```

The application will open in your browser.

You can then:

```text
Upload PDF
    ↓
Wait for processing
    ↓
Enter a question
    ↓
Retrieve relevant context
    ↓
Generate answer
```

---

# ☁️ Deployment

InsightRAG is deployed using **Streamlit Community Cloud**.

### Deployment Steps

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select the repository and branch.
5. Set `app.py` as the main application file.
6. Add the Gemini API key under **Advanced Settings → Secrets**.
7. Deploy the application.

### Streamlit Secret

Use:

```toml
GOOGLE_API_KEY = "your_gemini_api_key"
```

The API key should not be written directly into Python source code.

---

# 🔐 Security

InsightRAG keeps API credentials outside the source code.

### Local Development

```text
.env
```

is used for storing environment variables.

### Cloud Deployment

```text
Streamlit Secrets
```

is used to securely configure the Gemini API key.

Sensitive files and generated local data should not be committed to the repository.

---

# 🧪 Example

Suppose the user uploads:

```text
Machine_Learning_Notes.pdf
```

The system processes it:

```text
Machine_Learning_Notes.pdf
            ↓
       PDF Loader
            ↓
      Text Extraction
            ↓
      Text Chunking
            ↓
       Embeddings
            ↓
        FAISS Index
```

The user can then ask:

```text
What is supervised learning?
```

The retrieval system finds the most relevant document chunks:

```text
User Question
      ↓
Semantic Retrieval
      ↓
Relevant ML Notes
      ↓
RAG Prompt
      ↓
Gemini
      ↓
Answer
```

---

# 🎯 Why RAG?

A language model may have broad general knowledge, but it does not automatically have access to the contents of a user's private documents.

RAG addresses this by retrieving relevant information from the document and supplying it to the language model as context.

Instead of:

```text
Question → LLM → Answer
```

InsightRAG follows:

```text
Question
   ↓
Retrieve Relevant Information
   ↓
Augment Prompt With Context
   ↓
LLM
   ↓
Grounded Answer
```

This makes the application better suited for **document-specific question answering**.

---

# 💡 Key Engineering Concepts Demonstrated

InsightRAG demonstrates practical implementation of:

* Retrieval-Augmented Generation
* Semantic search
* Vector embeddings
* FAISS similarity search
* Document ingestion
* Text chunking
* Retrieval and reranking
* Prompt engineering
* LLM integration
* Modular Python architecture
* API key management
* Streamlit application development
* Cloud deployment

---

# ⚠️ Current Limitations

* Image-only or scanned PDFs may require OCR before useful text can be extracted.
* Retrieval quality depends on document quality, chunking, and embedding quality.
* Very large documents can require additional memory and processing time.
* LLM responses depend on the quality of the retrieved context.
* The current system is primarily designed for document-based question answering.

---

# 🔮 Future Improvements

Potential future improvements include:

* [ ] OCR support for scanned PDFs
* [ ] Page-level source citations
* [ ] Multi-PDF question answering
* [ ] Conversation memory
* [ ] Hybrid keyword + semantic retrieval
* [ ] Improved reranking strategies
* [ ] Retrieval evaluation metrics
* [ ] Answer confidence indicators
* [ ] Document metadata filtering
* [ ] Improved chunking strategies
* [ ] RAG evaluation using benchmark datasets

---

# 📈 Project Highlights

| Capability     | Implementation                            |
| -------------- | ----------------------------------------- |
| PDF Processing | PyPDF + LangChain                         |
| Text Chunking  | Recursive text splitting                  |
| Embeddings     | Configured embedding model                |
| Vector Search  | FAISS                                     |
| Retrieval      | Similarity-based retrieval                |
| Reranking      | Dedicated reranking module                |
| LLM            | Google Gemini                             |
| RAG Pipeline   | LangChain                                 |
| UI             | Streamlit                                 |
| Deployment     | Streamlit Community Cloud                 |
| Security       | Environment Variables + Streamlit Secrets |

---

# 👩‍💻 Author

## Arpita Tripathi

B.Tech. — Information Technology
Kamla Nehru Institute of Technology, Sultanpur

### GitHub

**https://github.com/ArpitaTrip1402**

---

# ⭐ Support

If you find **InsightRAG** useful or interesting, consider giving the repository a ⭐ 
on GitHub.

---

## 📌 Project Summary

**InsightRAG is a modular RAG-based document research system that combines PDF ingestion,
semantic embeddings, FAISS vector retrieval, context reranking, and Gemini-powered 
generation into a deployable Streamlit application.**
