import requests

HEADERS = {
    "User-Agent": "WikiRAGChatbot/1.0 (student project; contact: your-email@example.com)"
}

def search_wikipedia(query, limit=3):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": limit
    }
    response = requests.get(url, params=params, headers=HEADERS)
    data = response.json()
    results = data["query"]["search"]
    titles = [item["title"] for item in results]
    return titles

def get_article_content(title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "titles": title,
        "format": "json"
    }
    response = requests.get(url, params=params, headers=HEADERS)
    data = response.json()
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    content = page.get("extract", "")
    return content

if __name__ == "__main__":
    titles = search_wikipedia("Wright brothers first flight")
    print(titles)
    
    content = get_article_content(titles[0])
    print(content[:500])