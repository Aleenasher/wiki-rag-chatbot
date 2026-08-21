def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
        start += chunk_size - overlap
    
    return chunks


if __name__ == "__main__":
    from retriever import search_wikipedia, get_article_content
    
    titles = search_wikipedia("Wright brothers first flight")
    content = get_article_content(titles[0])
    
    chunks = chunk_text(content, chunk_size=100, overlap=20)
    
    print(f"Total words in article: {len(content.split())}")
    print(f"Number of chunks created: {len(chunks)}")
    print("\n--- First chunk ---")
    print(chunks[0])
    print("\n--- Second chunk ---")
    print(chunks[1])