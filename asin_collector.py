# asin_collector.py (modified to scrape 3 pages)

import requests
from bs4 import BeautifulSoup
import time

categories = {
    "Home & Kitchen": "https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/",
    "Electronics": "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
asin_list = []

def extract_asins_from_page(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.select('a.a-link-normal[href*="/dp/"]')

    asins = []
    for link in links:
        href = link.get('href')
        if '/dp/' in href:
            asin = href.split('/dp/')[1].split('/')[0]
            asins.append(asin)
    return list(set(asins))

# New: scrape multiple pages
for category, base_url in categories.items():
    print(f"Scraping category: {category}")
    for page_num in range(1, 4):  # First 3 pages
        url = f"{base_url}?pg={page_num}"
        asins = extract_asins_from_page(url)
        asin_list.extend(asins)
        time.sleep(1)

asin_list = list(set(asin_list))  # Remove duplicates

print(f"✅ Total ASINs collected: {len(asin_list)}")
print("Sample ASINs:", asin_list[:10])

with open("collected_asins.txt", "w") as f:
    for asin in asin_list:
        f.write(asin + "\n")

print("✅ ASINs saved to collected_asins.txt")
