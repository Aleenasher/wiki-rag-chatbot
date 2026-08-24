from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.create_collection(name="wiki_chunks")


def add_chunks_to_store(chunks):
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk]
        )


def search_chunks(query, top_k=3):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]


if __name__ == "__main__":
    from retriever import search_wikipedia, get_article_content
    from chunker import chunk_text

    titles = search_wikipedia("Wright brothers first flight")
    content = get_article_content(titles[0])
    chunks = chunk_text(content, chunk_size=300, overlap=50)

    print(f"Adding {len(chunks)} chunks to the vector store...")
    add_chunks_to_store(chunks)
    print("Done adding chunks.")

    query = "When did the Wright brothers first fly?"
    results = search_chunks(query, top_k=3)

    print(f"\nQuery: {query}")
    for i, r in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(r[:300])