
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

DB_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "agentverse_knowledge"


def get_embeddings():
    """Initialize local Hugging Face embeddings."""

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vector_store():
    """Return the ChromaDB vector store."""

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=DB_DIRECTORY,
    )


def ingest_text(
    text: str,
    source: str = "uploaded_document",
) -> int:
    """
    Split text into chunks and store them in ChromaDB.

    Returns the number of chunks created.
    """

    if not text.strip():
        raise ValueError("Document text cannot be empty.")

    document = Document(
        page_content=text,
        metadata={"source": source},
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
    )

    chunks = splitter.split_documents([document])

    vector_store = get_vector_store()
    vector_store.add_documents(chunks)

    return len(chunks)


if __name__ == "__main__":
    sample_text = """
    Scientific research into extraterrestrial life includes
    the search for habitable environments and possible
    biosignatures beyond Earth.

    Unidentified aerial phenomena are observations that
    have not yet been conclusively identified. An unidentified
    observation alone does not establish an extraterrestrial
    origin.

    Scientific conclusions should be based on reliable
    evidence, reproducible observations, and careful analysis.
    """

    count = ingest_text(
        text=sample_text,
        source="sample_science_document",
    )

    print(f"Successfully indexed {count} chunks.")
