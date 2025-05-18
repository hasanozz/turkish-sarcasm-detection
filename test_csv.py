import pandas as pd

df = pd.read_csv("veriler_zemberek.csv")       # köklenmiş
df_raw = pd.read_csv("veriler_duzgun.csv")     # orijinal hali


for i in range(5):  # ilk 5 örneğe bak
    print(f"\n--- Entry {i+1} ---")
    print("Ham metin:")
    print(df_raw['text'][i])
    print("\nKöklenmiş:")
    print(df['text'][i])
