def chunk_text(text, chunk_size=300, overlap=50):
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
    
    for size in [100, 300, 600]:
        chunks = chunk_text(content, chunk_size=size, overlap=int(size * 0.1))
        print(f"\nChunk size = {size} words:")
        print(f"  Number of chunks: {len(chunks)}")
        print(f"  Sample chunk (first 150 chars): {chunks[0][:150]}...")