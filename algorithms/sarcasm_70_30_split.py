import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import warnings
warnings.filterwarnings('ignore')

# === Dataset ===
df = pd.read_csv("csv_data/tfidf_dataset.csv")
X = df.drop(columns=["label"])
y = LabelEncoder().fit_transform(df["label"])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


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
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1-Score": f1_score(y_test, y_pred)
    })

results_df = pd.DataFrame(results)
print(results_df)


df_melted = results_df.melt(id_vars="Model", var_name="Metric", value_name="Score")
plt.figure(figsize=(12, 6))
sns.barplot(x="Model", y="Score", hue="Metric", data=df_melted, palette="Set2")

plt.title("Model Performans Karşılaştırması (TF-IDF, 70/30 Split)")
plt.xticks(rotation=45)
plt.ylim(0.4, 1.0)
plt.tight_layout()
plt.legend(loc='lower right')
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.savefig("results/70-30_split.png", dpi=300, bbox_inches='tight')
plt.show()