import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Dosyaları oku
df_zaytung = pd.read_csv("zaytung_sarcastic.csv")
df_trt = pd.read_csv("trt_news.csv")

# Sadece gerekli sütunların olduğundan emin ol
df_zaytung = df_zaytung[["source", "text", "label"]]
df_trt = df_trt[["source", "text", "label"]]

# Birleştir
df_merged = pd.concat([df_zaytung, df_trt], ignore_index=True)

# Karıştır (opsiyonel ama önerilir)
df_merged = df_merged.sample(frac=1, random_state=42).reset_index(drop=True)

# Kaydet
df_merged.to_csv("merged_dataset.csv", index=False, encoding="utf-8-sig")

print(f"Birleştirme tamamlandı. Toplam {len(df_merged)} kayıt → merged_dataset.csv")
