import streamlit as st
from retriever import search_wikipedia, get_article_content
from chunker import chunk_text
from vector_store import add_chunks_to_store, search_chunks
from generator import generate_answer

st.title("Wikipedia-Grounded Q&A Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

with st.form(key="question_form", clear_on_submit=True):
    question = st.text_input("Ask your question:")
    submitted = st.form_submit_button("Ask")

if submitted and question:
    with st.spinner("Searching Wikipedia..."):
        titles = search_wikipedia(question)
        content = get_article_content(titles[0])
        chunks = chunk_text(content, chunk_size=300, overlap=50)
        add_chunks_to_store(chunks, article_title=titles[0])

        answer = generate_answer(question)
        top_chunks = search_chunks(question, top_k=3)

    st.session_state.history.append({
        "question": question,
        "answer": answer,
        "chunks": top_chunks
    })

for entry in reversed(st.session_state.history):
    st.subheader(f"Q: {entry['question']}")
    st.write(entry["answer"])
    with st.expander("Source Passages Used"):
        for i, chunk in enumerate(entry["chunks"]):
            st.write(f"**Chunk {i+1}:**")
            st.write(chunk)
    st.divider()