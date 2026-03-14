import requests
from bs4 import BeautifulSoup
def get_temperature():
    """Scrape temperature from Tameteo using requests + BeautifulSoup"""
    url = "https://www.tameteo.com/meteo_Casablanca-Afrique-Maroc-Dukala+Abda-GMMC-1-9765.html"

    # Get page HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the span with the class
    span = soup.find("span", class_="dato-temperatura changeUnitT")

    if span:
        print("Temperature:", span.text.strip())
        return span.text.strip()
    else:
        print("Temperature not found")
