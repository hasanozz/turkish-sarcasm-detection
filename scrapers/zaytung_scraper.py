from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# === url ve çekilecek veri sayısı ===
BASE_URL = "https://www.zaytung.com/digerleri.asp?pg="
TOTAL_PAGES = 338  # ortalama 3.4k veri falan
WAIT_TIME = 2

# === chrome driver ===
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

data = []

for page in range(1, TOTAL_PAGES + 1):
    url = BASE_URL + str(page)
    driver.get(url)
    time.sleep(WAIT_TIME)

    print(f"Sayfa {page} yükleniyor...")

    try:
        # td[align = 'left'] > h3 > a olan verileri çek (haber başlıklara denk geliyor)
        elements = driver.find_elements(By.CSS_SELECTOR, 'td[align="left"] h3 a')
        for el in elements:
            text = el.text.strip()
            if text:
                data.append({
                    "source": "zaytung",
                    "text": text,
                    "label": "sarcastic"
                })
        print(f"Sayfa {page}: {len(elements)} başlık bulundu.")
    except Exception as e:
        print(f"Sayfa {page} atlandı: {e}")

driver.quit()

# csv kaydet
df = pd.DataFrame(data)
df.to_csv("zaytung_sarcastic.csv", index=False, encoding="utf-8-sig")
print(f"İşlem tamamlandı! Toplam: {len(data)} başlık çekildi.")
