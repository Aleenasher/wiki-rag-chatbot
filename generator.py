import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
from vector_store import search_chunks


def generate_answer(question, top_k=3):
    chunks = search_chunks(question, top_k=top_k)

    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[Chunk {i+1}]: {chunk}\n\n"

    system_prompt = """You are a factual Q&A assistant. You must follow these rules strictly:
1. Answer ONLY using the information in the provided context below.
2. Do NOT use any knowledge from your own training data.
3. For every claim you make, cite which chunk it came from, like [Chunk 1].
4. If the context does not contain enough information to answer the question, 
   say exactly: "I don't have enough information in the retrieved context to answer this question."
   Do not guess or make anything up.
"""

    user_prompt = f"""Context:
{context}

Question: {question}

Answer using only the context above, with citations."""

    response = client.chat.completions.create(
       model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content
if __name__ == "__main__":
    from retriever import search_wikipedia, get_article_content
    from chunker import chunk_text
    from vector_store import add_chunks_to_store

    titles = search_wikipedia("Wright brothers first flight")
    content = get_article_content(titles[0])
    chunks = chunk_text(content, chunk_size=300, overlap=50)
    add_chunks_to_store(chunks)

    question = "When did the Wright brothers first fly?"
    answer = generate_answer(question)

    print(f"Question: {question}")
    print(f"\nAnswer:\n{answer}")