import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

BASE_URL = "https://quotes.toscrape.com"

def scrape_author_bios():
    authors = {}
    
    # Step 1: Get all quotes and author links
    page = 1
    while True:
        url = f"{BASE_URL}/page/{page}/"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code != 200:
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select('div.quote')
        
        if not cards:
            break
            
        for card in cards:
            author_link = card.select_one('a[href^="/author/"]')
            if author_link:
                author_url = urljoin(BASE_URL, author_link['href'])
                if author_url not in authors:
                    authors[author_url] = None  # placeholder
        
        page += 1
        time.sleep(1)  # Be polite
    
    # Step 2: Visit each author page and get bio
    print(f"Found {len(authors)} unique authors. Scraping bios...")
    
    data = []
    for i, (author_url, _) in enumerate(authors.items(), 1):
        try:
            resp = requests.get(author_url, headers={'User-Agent': 'Mozilla/5.0'})
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                name = soup.select_one('h3.author-title').get_text(strip=True)
                bio = soup.select_one('div.author-description').get_text(strip=True)
                
                data.append([name, bio])
                print(f"{i:2d}. Scraped: {name}")
        except:
            pass
        time.sleep(1)
    
    # Step 3: Save to CSV
    with open('author_bios.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Author Name', 'Bio'])
        writer.writerows(data)
    
    print(f"\n✅ Done! Saved {len(data)} author bios to author_bios.csv")
    return len(data)

if __name__ == "__main__":
    scrape_author_bios()
