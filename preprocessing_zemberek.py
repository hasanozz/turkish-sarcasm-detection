import pandas as pd
import jpype
import jpype.imports
from jpype.types import JString
import os
import re

# JVM ve JAR yolları
jar_path = os.path.join(os.getcwd(), "zemberek-full.jar")
jvm_path = r"C:\Program Files\Java\jdk-24\bin\server\jvm.dll"

if not jpype.isJVMStarted():
    jpype.startJVM(
        jvm_path,
        "--enable-native-access=ALL-UNNAMED",
        "-ea",
        f"-Djava.class.path={jar_path}"
    )

# Zemberek sınıfı
TurkishMorphology = jpype.JClass("zemberek.morphology.TurkishMorphology")
morphology = TurkishMorphology.createWithDefaults()

# Ön temizlik
def clean_text(text):
    text = str(text)

    # 1. bkz yapıları temizle
    text = re.sub(r"\(bkz:[^)]+\)", "", text)
    text = re.sub(r"\bbkz\b:?", "", text, flags=re.IGNORECASE)

    # 2. linkleri temizle
    text = re.sub(r"http\S+", "", text)

    # 3. tırnak içinde boş entry'leri temizle
    text = re.sub(r'^""$', '', text.strip())
    text = re.sub(r'^\'\'$', '', text.strip())

    # 4. noktalama & özel karakter temizliği
    text = re.sub(r"[^\w\sçğıöşüÇĞİÖŞÜ]", "", text)
    
    # 5. sayıları temizle
    text = re.sub(r"\d+", "", text)

    # 6. çoklu boşlukları azalt
    text = re.sub(r"\s+", " ", text)

    # 7. Küçük harfe çevir
    return text.lower().strip()


# Kök bulma (UNK-savar)
def get_roots(text):
    words = text.split()
    roots = []
    for word in words:
        try:
            analysis = morphology.analyzeSentence(JString(word))
            results = morphology.disambiguate(JString(word), analysis).bestAnalysis()
            if results and results[0].getLemmas():
                lemma = str(results[0].getLemmas()[0])
                if lemma.lower() in ['unk', 'unknown', 'unkn', 'none', 'null']:
                    roots.append(word)
                else:
                    roots.append(lemma)
            else:
                roots.append(word)
        except:
            roots.append(word)
    return " ".join(roots)

# CSV oku
df = pd.read_csv("veriler_duzgun.csv")
cleaned_entries = []

# Entry'lere uygula
for i, text in enumerate(df['text']):
    try:
        raw = clean_text(text)
        root_text = get_roots(raw)
        cleaned_entries.append(root_text)
    except Exception as e:
        print(f"Hata satır {i}: {e}")
        cleaned_entries.append("")

# CSV yaz
df_out = pd.DataFrame({'text': cleaned_entries})
df_out.to_csv("veriler_zemberek.csv", index=False, encoding="utf-8-sig")

print("✅ Zemberek kök çıkarımı TAMAMLANDI.")
print("💾 veriler_zemberek.csv oluşturuldu.")
