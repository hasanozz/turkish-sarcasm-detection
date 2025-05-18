from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

# chromedriver yolunu ayarla
driver_path = os.path.join(os.getcwd(), "chromedriver.exe")

options = Options()
# options.add_argument("--headless")  # İstersen açarsın
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Hedef başlık: türkiye ekonomisi
BASE_URL = "https://eksisozluk.com/turkiye-ekonomisi--115645?p="

entries = []

for page in range(1, 101):  # 100 sayfa = ~1000 entry
    url = BASE_URL + str(page)
    driver.get(url)
    time.sleep(2.5)

    # Her entry bir <li> içinde yer alıyor
    entry_items = driver.find_elements(By.XPATH, '//ul[@id="entry-item-list"]/li')
    for item in entry_items:
        try:
            content = item.find_element(By.CLASS_NAME, "content").text.strip()
            if content:
                entries.append(content)
        except:
            continue

    print(f"✅ Sayfa {page} tamamlandı – Toplam entry: {len(entries)}")

driver.quit()

# CSV'ye yaz
df = pd.DataFrame({"text": entries})
df.to_csv("veriler_duzgun.csv", index=False, encoding="utf-8-sig")

print("🎯 Final entry sayısı:", len(entries))
print("✅ Kaydedildi: veriler_duzgun.csv")
