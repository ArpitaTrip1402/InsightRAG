"""
InsightRAG — Intelligent Document Research
--------------------------------------------
This is the UI layer only. All backend logic (ingestion, embeddings,
vector store, retrieval, generation) lives in the existing modules and
is called here exactly as before — no backend architecture was changed.
"""

import os
import streamlit as st

# ---------------------------------------------------------------------
# Existing backend imports — unchanged from the original project
# ---------------------------------------------------------------------
from ingestion.loader import load_pdf
from ingestion.splitter import split_documents
from embeddings.embedder import get_embedding_model
from vectorstore.faiss_store import create_vector_store
from retrieval.retriever import get_retriever
from generation.prompt import get_rag_prompt
from generation.llm import get_llm
from generation.rag_chain import create_rag_chain


# =======================================================================
# PAGE CONFIG
# =======================================================================
st.set_page_config(
    page_title="InsightRAG",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =======================================================================
# CUSTOM CSS — sophisticated, minimal, "serious AI product" aesthetic
# =======================================================================
def inject_custom_css():
    st.markdown(
        """
        <style>
            :root {
                --bg: #EFE3D4;
                --surface: #FBF6EF;
                --border: #DCCBB4;
                --text-primary: #000000;
                --text-secondary: #3A3530;
                --accent: #6B4226;
                --accent-soft: #F0E4D6;
                --radius: 14px;
            }

            /* Overall app background — nude tone for the main content area */
            .stApp {
                background: var(--bg);
            }

            /* Hide default Streamlit chrome for a cleaner product feel */
            /* Hide the hamburger menu and footer, but keep the header bar
               itself intact — it's what holds the "reopen sidebar" arrow
               once the sidebar has been collapsed. */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header[data-testid="stHeader"] {
                background: transparent;
            }
            /* Make sure the reopen-sidebar arrow is never accidentally hidden */
            [data-testid="collapsedControl"] {
                visibility: visible !important;
                display: flex !important;
            }

            /* Sidebar — solid brown */
            section[data-testid="stSidebar"] {
                background: #5C4033;
                border-right: 1px solid var(--border);
            }

            /* Default text inside the sidebar reads white against the gradient */
            section[data-testid="stSidebar"] label,
            section[data-testid="stSidebar"] p,
            section[data-testid="stSidebar"] span,
            section[data-testid="stSidebar"] div {
                color: #FFFFFF;
            }

            /* Generic card */
            .ir-card {
                background-color: var(--surface);
                border: 1px solid var(--border);
                border-radius: var(--radius);
                padding: 1.25rem 1.5rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            }

            /* Brand header in sidebar */
            .ir-brand {
                font-size: 1.15rem;
                font-weight: 700;
                color: #FFFFFF !important;
                margin-bottom: 0.1rem;
            }
            .ir-brand-sub {
                font-size: 0.8rem;
                color: rgba(255,255,255,0.75) !important;
                margin-bottom: 1.5rem;
            }

            /* Upload dropzone — frosted glass look against the blue gradient */
            .ir-upload-empty {
                border: 1.5px dashed rgba(255,255,255,0.4);
                border-radius: var(--radius);
                padding: 2rem 1rem;
                text-align: center;
                color: rgba(255,255,255,0.85) !important;
                background-color: rgba(255,255,255,0.08);
            }
            .ir-upload-empty div {
                color: rgba(255,255,255,0.85) !important;
            }
            .ir-upload-empty .icon {
                font-size: 1.6rem;
                color: #FFFFFF;
                margin-bottom: 0.4rem;
            }

            /* Streamlit's native file-uploader box, restyled to match */
            section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
                background-color: rgba(255,255,255,0.08);
                border: 1.5px dashed rgba(255,255,255,0.4);
                border-radius: var(--radius);
            }
            section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
                background-color: #000000;
                color: #FFFFFF;
                border: none;
            }
            section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button:hover {
                background-color: #1A1A1A;
                color: #FFFFFF;
            }

            /* Document status card — always dark text on its white surface,
               regardless of the blue gradient behind it in the sidebar */
            .ir-card, .ir-card * {
                color: var(--text-primary) !important;
            }
            .ir-doc-name {
                font-weight: 600;
                font-size: 0.95rem;
                margin-bottom: 0.2rem;
            }
            .ir-doc-ready {
                color: #16794B !important;
                font-size: 0.8rem;
                margin-bottom: 1rem;
            }
            .ir-stat-row {
                display: flex;
                justify-content: space-between;
                font-size: 0.85rem;
                padding: 0.35rem 0;
                border-bottom: 1px solid var(--border);
                color: var(--text-secondary) !important;
            }
            .ir-stat-row span.value {
                color: var(--text-primary) !important;
                font-weight: 600;
            }

            /* Main header — big centered title + subheading */
            .ir-greeting {
                font-size: 2.4rem;
                font-weight: 800;
                color: var(--text-primary);
                text-align: center;
                margin-bottom: 0.4rem;
            }
            .ir-subtext {
                color: var(--text-secondary);
                font-size: 1.05rem;
                text-align: center;
                margin-bottom: 1.8rem;
                line-height: 1.5;
            }

            /* Empty state */
            .ir-empty-wrap {
                text-align: center;
                padding: 3rem 1rem 2rem 1rem;
            }
            .ir-empty-mark {
                font-size: 1.8rem;
                color: var(--accent);
            }
            .ir-empty-title {
                font-size: 1.2rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-top: 0.5rem;
            }
            .ir-empty-sub {
                color: var(--text-secondary);
                margin-top: 0.3rem;
                margin-bottom: 1.5rem;
            }

            /* Answer card */
            .ir-answer-label {
                font-size: 0.75rem;
                letter-spacing: 0.06em;
                font-weight: 700;
                color: var(--accent);
                margin-bottom: 0.6rem;
            }
            .ir-answer-text {
                font-size: 1rem;
                color: var(--text-primary);
                line-height: 1.65;
            }
            .ir-divider {
                border: none;
                border-top: 1px solid var(--border);
                margin: 1.1rem 0;
            }
            .ir-sources-label {
                font-size: 0.75rem;
                letter-spacing: 0.06em;
                font-weight: 700;
                color: var(--text-secondary);
                margin-bottom: 0.5rem;
            }
            .ir-source-row {
                display: flex;
                justify-content: space-between;
                font-size: 0.85rem;
                color: var(--text-secondary);
                padding: 0.3rem 0;
            }

            /* Buttons */
            .stButton > button {
                border-radius: 10px;
                border: 1px solid var(--border);
                background-color: var(--surface);
                color: var(--text-primary);
                font-weight: 500;
            }
            .stButton > button:hover {
                border-color: var(--accent);
                color: var(--accent);
            }

            /* Primary ask button */
            div[data-testid="stFormSubmitButton"] > button {
                background-color: var(--accent);
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: 600;
            }
            div[data-testid="stFormSubmitButton"] > button:hover {
                background-color: #4A2F1F;
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =======================================================================
# CACHED BACKEND RESOURCES
# Embedding model and LLM are expensive to load and are identical across
# every user/document, so they are cached globally with @st.cache_resource.
# The vector store depends on the uploaded document, so it is built once
# per document and stored in st.session_state instead (see process_document).
# =======================================================================
@st.cache_resource(show_spinner=False)
def load_embedding_model():
    return get_embedding_model()


@st.cache_resource(show_spinner=False)
def load_llm():
    return get_llm()


# =======================================================================
# SESSION STATE INITIALIZATION
# =======================================================================
def init_session_state():
    defaults = {
        "document_processed": False,
        "doc_name": None,
        "num_pages": 0,
        "num_chunks": 0,
        "rag_chain": None,
        "last_answer": None,
        "last_sources": None,
        "question_input": "",
        "prefill_question": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =======================================================================
# DOCUMENT PROCESSING PIPELINE
# Runs the existing backend pipeline once per uploaded document:
# PDF -> load_pdf -> split_documents -> embeddings -> FAISS -> retriever
# -> prompt -> llm -> rag_chain
# =======================================================================
def process_document(uploaded_file):
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    status_box = st.empty()

    with status_box.container():
        with st.status("Processing document...", expanded=True) as status:
            st.write("⟳ Reading document")
            documents = load_pdf(file_path)

            st.write("⟳ Creating chunks")
            chunks = split_documents(documents)

            st.write("⟳ Generating embeddings")
            embedding_model = load_embedding_model()
            
            print("=" * 60)
            print(f"NUMBER OF CHUNKS: {len(chunks)}")
            print("=" * 60)

            if chunks:
              print("FIRST CHUNK:")
              print(chunks[0].page_content[:500])
            else:
              print("ERROR: chunks is EMPTY") 

            vector_store = create_vector_store(chunks, embedding_model)

            retriever = get_retriever(vector_store)
            prompt = get_rag_prompt()
            llm = load_llm()
            rag_chain = create_rag_chain(retriever, prompt, llm)

            status.update(label="✓ Document ready", state="complete", expanded=False)

    status_box.empty()

    st.session_state.document_processed = True
    st.session_state.doc_name = uploaded_file.name
    st.session_state.num_pages = len(documents)
    st.session_state.num_chunks = len(chunks)
    st.session_state.rag_chain = rag_chain
    st.session_state.last_answer = None
    st.session_state.last_sources = None


# =======================================================================
# SIDEBAR — branding, upload, document status
# =======================================================================
def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="ir-brand">✦ InsightRAG</div>
            <div class="ir-brand-sub">Intelligent Document Research</div>
            """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Upload your document",
            type=["pdf"],
            label_visibility="collapsed",
        )

        if uploaded_file is not None and uploaded_file.name != st.session_state.doc_name:
            process_document(uploaded_file)

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        render_document_status()


def render_document_status():
    if not st.session_state.document_processed:
        st.markdown(
            """
            <div class="ir-upload-empty">
                <div class="icon">⬆</div>
                <div>No document uploaded yet</div>
                <div style="font-size:0.8rem; margin-top:0.3rem;">PDF files supported</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"""
        <div class="ir-card">
            <div class="ir-doc-name">📄 {st.session_state.doc_name}</div>
            <div class="ir-doc-ready">✓ Ready for analysis</div>
            <div class="ir-stat-row"><span>Pages</span><span class="value">{st.session_state.num_pages}</span></div>
            <div class="ir-stat-row"><span>Chunks</span><span class="value">{st.session_state.num_chunks}</span></div>
            <div class="ir-stat-row" style="border-bottom:none;"><span>Status</span><span class="value">● Ready</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =======================================================================
# MAIN AREA — header, empty state, question input, answer, sources
# =======================================================================
def render_header():
    st.markdown(
        """
        <div class="ir-greeting">📚 InsightRAG</div>
        <div class="ir-subtext">
            Intelligent Document Research &amp; Q&amp;A System
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state():
    st.markdown(
        """
        <div class="ir-empty-wrap">
            <div class="ir-empty-mark">✦</div>
            <div class="ir-empty-title">Your document is ready</div>
            <div class="ir-empty-sub">Ask InsightRAG anything about the content of your document.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    suggestions = ["Summarize the document", "What are the key points?", "Find important facts"]
    for col, suggestion in zip([col1, col2, col3], suggestions):
        with col:
            if st.button(suggestion, use_container_width=True):
                st.session_state.prefill_question = suggestion
                st.rerun()


def render_question_input():
    # Apply a pre-filled question from an example button, if one was clicked.
    if st.session_state.prefill_question:
        st.session_state.question_input = st.session_state.prefill_question
        st.session_state.prefill_question = None

    with st.form(key="question_form", clear_on_submit=False):
        question = st.text_input(
            "Ask anything about your document...",
            key="question_input",
            label_visibility="collapsed",
            placeholder="Ask anything about your document...",
        )
        submitted = st.form_submit_button("Ask ↑")

    if submitted and question.strip():
        answer_question(question.strip())


def answer_question(question: str):
    with st.spinner("Thinking..."):
        rag_chain = st.session_state.rag_chain
        result = rag_chain.invoke(question)

        # The rag_chain may return a plain string, or an object/dict that
        # also carries retrieved source documents. Both cases are handled
        # here so source display can be wired in cleanly once available.
        answer_text = None
        source_documents = None

        if isinstance(result, str):
            answer_text = result
        elif isinstance(result, dict):
            answer_text = result.get("answer") or result.get("result") or str(result)
            source_documents = result.get("source_documents")
        else:
            answer_text = getattr(result, "content", str(result))
            source_documents = getattr(result, "source_documents", None)

        st.session_state.last_answer = answer_text
        st.session_state.last_sources = source_documents


def render_answer():
    if not st.session_state.last_answer:
        return

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="ir-card">', unsafe_allow_html=True)
    st.markdown('<div class="ir-answer-label">✦ ANSWER</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ir-answer-text">{st.session_state.last_answer}</div>', unsafe_allow_html=True)

    if st.session_state.last_sources:
        st.markdown('<hr class="ir-divider">', unsafe_allow_html=True)
        render_sources(st.session_state.last_sources)

    st.markdown("</div>", unsafe_allow_html=True)


def render_sources(source_documents):
    st.markdown('<div class="ir-sources-label">📚 SOURCES</div>', unsafe_allow_html=True)
    for doc in source_documents:
        # document.metadata is preserved exactly as produced by the loader,
        # so page/source info stays available for citation display.
        source_name = doc.metadata.get("source", st.session_state.doc_name)
        page = doc.metadata.get("page")
        page_label = f"Page {page + 1}" if isinstance(page, int) else "—"
        st.markdown(
            f'<div class="ir-source-row"><span>📄 {os.path.basename(str(source_name))}</span><span>{page_label}</span></div>',
            unsafe_allow_html=True,
        )


# =======================================================================
# APP ENTRY POINT
# =======================================================================
def main():
    inject_custom_css()
    init_session_state()

    render_sidebar()
    render_header()

    if not st.session_state.document_processed:
        st.info("Upload a PDF from the sidebar to get started.")
        return

    if not st.session_state.last_answer:
        render_empty_state()

    render_question_input()
    render_answer()


if __name__ == "__main__":
    main()