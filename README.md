Wikipedia-Grounded Q&A Chatbot

A RAG (Retrieval-Augmented Generation) chatbot that answers questions using only Wikipedia content, and says "I don't know" when it can't find the answer instead of making something up.

Problem

LLMs hallucinate. If you ask ChatGPT something specific, it'll often give you a confident, fluent, wrong answer. This project builds a Q&A system that only answers from Wikipedia content it actually retrieved, and refuses to answer if that content doesn't cover the question.

How It Works

1. Take the user's question and search Wikipedia for a relevant article
2. Split the article into overlapping chunks (300 words, 50-word overlap)
3. Embed each chunk and store it in ChromaDB
4. Embed the question and retrieve the top 3 most similar chunks
5. Send those chunks to an LLM with strict instructions to only use that context
6. Show the answer along with the actual source chunks used

Tech Stack

- Wikipedia REST API for retrieval
- sentence-transformers (all-MiniLM-L6-v2) for embeddings
- ChromaDB as the vector store
- Groq API (openai/gpt-oss-20b) for generation
- Streamlit for the UI

Setup

git clone https://github.com/Aleenasher/wiki-rag-chatbot.git
cd wiki-rag-chatbot

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install requests sentence-transformers chromadb streamlit groq python-dotenv

Create a .env file in the project root:
GROQ_API_KEY=your_key_here

Get a free key at console.groq.com.

Running

streamlit run app.py

Individual files can also be run on their own for testing:
python retriever.py
python chunker.py
python vector_store.py
python generator.py

Why These Choices

Chunk size = 300 words: Tried 100, 300, and 600. 100 was too precise and cut sentences off mid-thought. 600 kept full context but pulled in too much irrelevant text. 300 was the best middle ground.

top_k = 3: Enough chunks to usually contain the answer, without flooding the LLM with unrelated context.

Chunk IDs include the article title: Originally chunks were just numbered 0, 1, 2... which meant chunks from a new article would overwrite chunks from a previous one in ChromaDB. Fixed by using {article_title}_{index} as the ID instead.

Refusal instead of guessing: The system prompt tells the LLM to say it doesn't have enough information if the retrieved chunks don't answer the question. Tested this with an out-of-context question (capital of France) and it correctly refused instead of using its own knowledge.

Known Limitations

- Only pulls one Wikipedia article per question, so questions needing info from multiple articles won't get full context.
- No memory between questions — each one is handled independently, so follow-ups don't carry context from the previous question.
- Semantic search sometimes surfaces a related-but-not-quite-right chunk alongside the correct one for very specific factual questions.

Status

Core pipeline (retrieval, chunking, embeddings, grounded generation, UI) is complete and working.
