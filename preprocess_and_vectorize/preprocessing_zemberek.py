import pandas as pd
import jpype
import jpype.imports
from jpype.types import JString
import os
import re
from tqdm import tqdm
import sys

sys.stdout.reconfigure(encoding='utf-8')

jar_path = os.path.join(os.getcwd(), "zemberek-full.jar")
jvm_path = r"C:\Program Files\Java\jdk-24\bin\server\jvm.dll"

if not jpype.isJVMStarted():
    jpype.startJVM(
        jvm_path,
        "--enable-native-access=ALL-UNNAMED",
        "-ea",
        f"-Djava.class.path={jar_path}"
    )

TurkishMorphology = jpype.JClass("zemberek.morphology.TurkishMorphology")
morphology = TurkishMorphology.createWithDefaults()

stopwords = set("""
acaba ama ancak aslında az bazı belki beri bile bütün çünkü daha de defa değil diye dokuz dört eğer en fakat gibi göre hem hep hatta hiç ile ise kez ki kim kimse madem mi mu mı mü nasıl ne neden nedenle nerde nerede nereye niçin niye o sanki sekiz sen senin siz sizin sonra ta tüm üç ve veya ya yalnız yedi yine yok yoksa yüzyıl zaman
""".split())

def clean_text(text):
    text = str(text)
    text = re.sub(r"\(bkz:[^)]+\)", "", text)
    text = re.sub(r"\bbkz\b:?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r'^["\']{2}$', '', text.strip())
    text = re.sub(r"[^\w\sçğıöşüÇĞİÖŞÜ]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()


def get_roots_cleaned(text):
    if not text or pd.isna(text) or text.strip() == "":
        return ""
    try:
        analysis = morphology.analyzeAndDisambiguate(JString(text))
        lemmas = []
        for result in analysis.bestAnalysis():
            lemma = str(result.getLemmas()[0])
            if lemma.lower() in ["unk", "unknown", "unkn", "null", "none"]:
                lemma = result.getStem()
            if 3 <= len(lemma) <= 30 and lemma not in stopwords:
                lemmas.append(lemma)
        return " ".join(lemmas)
    except:
        return text

df = pd.read_csv("merged_dataset.csv")
processed_texts = []

for text in tqdm(df['text'], desc="Ön işleme"):
    try:
        cleaned = clean_text(text)
        rooted = get_roots_cleaned(cleaned)
        processed_texts.append(rooted)
    except Exception as e:
        processed_texts.append("")

df_out = df.copy()
df_out["text"] = processed_texts
df_out.to_csv("preprocessed_data.csv", index=False, encoding="utf-8-sig")
print("\npreprocess bitti.")
