import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import os
import warnings

warnings.filterwarnings('ignore')


df = pd.read_csv("csv_data/tfidf_dataset.csv")
X = df.drop(columns=["label"])
y = LabelEncoder().fit_transform(df["label"])


models = {
    "Naive Bayes": MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree (J48)": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "AdaBoostM1": AdaBoostClassifier(),
    "SVM": SVC(),
    "Extra Trees": RandomForestClassifier(n_estimators=50, max_depth=5)
}


results = []
for name, model in models.items():
    model.fit(X, y)  # Tüm veriyle eğit
    y_pred = model.predict(X)  # Tahmin yine aynı veri üzerinden

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y, y_pred),
        "Precision": precision_score(y, y_pred),
        "Recall": recall_score(y, y_pred),
        "F1-Score": f1_score(y, y_pred)
    })

results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by="Accuracy", ascending=False)


print(results_df)


os.makedirs("results", exist_ok=True)
plt.figure(figsize=(12, 6))
sns.barplot(data=results_df.melt(id_vars="Model", var_name="Metric", value_name="Score"),
            x="Model", y="Score", hue="Metric")
plt.title("Model Performansı (%100 Eğitim Verisi Üzerinde)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("results/100_training_split.png", dpi=300, bbox_inches='tight')
plt.show()
