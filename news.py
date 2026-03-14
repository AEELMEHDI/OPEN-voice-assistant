import requests
from bs4 import BeautifulSoup

def get_news(limit=10):
    """Scrape Hespress (Société) headlines using requests + BeautifulSoup"""
    url = "https://fr.hespress.com/societe"

    # Send request to the website
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()  # Raise error if failed

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find headlines (they are in <h3> tags on Hespress)
    headlines = []
    for i, h3 in enumerate(soup.find_all("h3")[:limit], start=1):
        headlines.append(h3.get_text(strip=True))

    # Return as a string (for speak)
    news= " . ".join(headlines)
    return news

# Example usage
#if __name__ == "__main__":
    ##news = get_news(5)
    #print("Latest News:", news)
