from docx import Document
import chromadb
from sentence_transformers import SentenceTransformer

def load_document(path):
    doc = Document(path)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())
    return full_text
client = chromadb.Client()
collection = client.create_collection("apex_docs")

model = SentenceTransformer("all-MiniLM-L6-v2")
def store_chunks(chunks):
    embeddings = model.encode(chunks).tolist()
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[str(i) for i in range(len(chunks))]
    )


def search(query, n_results=3):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    return results["documents"][0]



def setup_rag(doc_path):
    chunks = load_document(doc_path)
    store_chunks(chunks)
    return "RAG setup complete!"