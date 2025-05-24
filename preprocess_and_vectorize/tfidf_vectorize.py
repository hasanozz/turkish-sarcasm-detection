import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import sys

sys.stdout.reconfigure(encoding='utf-8')


df = pd.read_csv("preprocessed_data.csv")


vectorizer = TfidfVectorizer(
    max_features=1000,       # En çok bilgi taşıyan 1000 kelime
    ngram_range=(1,2),       # Unigram + Bigram
    min_df=5,                # En az 5 belgede geçen kelimeler
    max_df=0.8,              # En fazla %80 belgede geçen kelimeler
)


X_tfidf = vectorizer.fit_transform(df["text"].fillna("")).toarray()


tfidf_df = pd.DataFrame(X_tfidf, columns=vectorizer.get_feature_names_out())


tfidf_df["label"] = df["label"]


tfidf_df.to_csv("tfidf_dataset.csv", index=False, encoding="utf-8-sig")
print("TF-IDF vektörleri tfidf_dataset.csv dosyasına kaydedildi.")
