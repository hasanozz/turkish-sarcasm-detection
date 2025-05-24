import requests
from bs4 import BeautifulSoup
import csv
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://www.trthaber.com/haber/gundem/{}.sayfa.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_trt_news(pages=20, delay=1):
    data = []

    for page in range(1, pages + 1):
        url = BASE_URL.format(page)
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Sayfa {page} alınamadı! Status Code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        
        # div.left > div.title > a içindeki texti al
        titles = soup.select("div.left div.title a")

        for tag in titles:
            text = tag.get("title")
            if text:
                data.append({
                    "source": "trt",
                    "text": text.strip(),
                    "label": "non-sarcastic"
                })

        print(f"Sayfa {page} tamamlandı.")
        time.sleep(delay)  # sunucuyu yormamak için

    # csvye kaydetme
    with open("trt_news.csv", "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "text", "label"])
        writer.writeheader()
        writer.writerows(data)

    print(f"\nToplam {len(data)} haber başlığı kaydedildi → trt_news.csv")

# run
if __name__ == "__main__":
    scrape_trt_news(pages=350)
