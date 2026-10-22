
"""AsEl-AI capstone: policy document retrieval pipeline."""

from pathlib import Path
import re

import chromadb
from sentence_transformers import SentenceTransformer

# Current repository structure:
# backend/dataset.py
# backend/backend/knowledge_base/*.md
ROOT = Path(__file__).resolve().parent
KNOWLEDGE_BASE = ROOT / "backend" / "knowledge_base"
CHROMA_PATH = ROOT / "chroma_db"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_documents():
    """Load Markdown policy documents from the knowledge base."""
    files = sorted(KNOWLEDGE_BASE.glob("*.md"))
    if not files:
        raise FileNotFoundError(
            f"No Markdown policies found in {KNOWLEDGE_BASE}. "
            "Check the repository folder structure."
        )

    documents = []
    for file in files:
        text = file.read_text(encoding="utf-8").strip()
        if text:
            documents.append({
                "id": file.stem,
                "text": text,
                "source": file.name,
            })

    if len(documents) < 12:
        raise ValueError(
            f"Expected 12 policy documents; found {len(documents)}."
        )
    return documents


def chunk_text(text, strategy="fixed", size=500, overlap=80):
    """Split text using fixed-size or paragraph-based chunking."""
    if strategy == "fixed":
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + size, len(text))
            chunks.append(text[start:end])
            if end == len(text):
                break
            start = end - overlap
        return chunks

    if strategy == "paragraph":
        paragraphs = [
            p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()
        ]
        return paragraphs or [text]

    raise ValueError("strategy must be 'fixed' or 'paragraph'")


def build_index(strategy="fixed"):
    """Create or refresh a ChromaDB collection for one chunking strategy."""
    documents = load_documents()
    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(
        name=f"healthcare_policies_{strategy}"
    )

    ids, texts, metadatas = [], [], []
    for document in documents:
        chunks = chunk_text(document["text"], strategy=strategy)
        for index, chunk in enumerate(chunks):
            ids.append(f"{document['id']}_{strategy}_{index}")
            texts.append(chunk)
            metadatas.append({
                "source": document["source"],
                "strategy": strategy,
                "chunk_index": index,
            })

    # Upsert makes rerunning this script safe.
    embeddings = model.encode(texts, normalize_embeddings=True).tolist()
    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )
    return collection, model


def search_policies(question, collection, model, top_k=3):
    """Retrieve the most relevant policy chunks for a question."""
    query_embedding = model.encode(
        [question], normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
    )

    matches = []
    if results["documents"]:
        for text, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            matches.append({
                "text": text,
                "source": metadata["source"],
                "distance": distance,
            })
    return matches


if __name__ == "__main__":
    for strategy in ("fixed", "paragraph"):
        collection, model = build_index(strategy)
        print(f"\nStrategy: {strategy}")
        print(f"Indexed chunks: {collection.count()}")

        question = "What should a patient do in a medical emergency?"
        results = search_policies(question, collection, model)

        for result in results:
            print(f"\nSource: {result['source']}")
            print(result["text"])
