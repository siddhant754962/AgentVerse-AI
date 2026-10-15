
from langchain_chroma import Chroma

from rag.ingest import (
    get_embeddings,
    DB_DIRECTORY,
    COLLECTION_NAME,
)


def get_retriever():
    """Initialize the existing ChromaDB collection."""

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=DB_DIRECTORY,
    )


def retrieve_context(query: str, k: int = 3) -> list[dict]:
    """Retrieve relevant document chunks from ChromaDB."""

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if k < 1:
        raise ValueError("k must be at least 1.")

    vector_store = get_retriever()
    documents = vector_store.similarity_search(query, k=k)

    return [
        {
            "source_type": "uploaded_document",
            "title": document.metadata.get(
                "source", "Uploaded Document"
            ),
            "url": "",
            "content": document.page_content,
        }
        for document in documents
    ]


if __name__ == "__main__":
    query = "What does an unidentified observation prove?"
    results = retrieve_context(query, k=3)

    if not results:
        print("No relevant documents found.")

    for index, result in enumerate(results, start=1):
        print(f"\n===== DOCUMENT {index} =====")
        print("Source:", result["title"])
        print("Content:", result["content"])
