# Turkish Sarcasm Detection with Machine Learning

## About the Project

This project focuses on detecting **sarcasm** in Turkish news headlines using machine learning methods. The dataset consists of two sources: humorous content from **Zaytung** and serious news content from **TRT Haber**. The goal is to classify texts as sarcastic or non-sarcastic based on supervised learning techniques.

## Methodology

- **Data Collection:**  
  - Zaytung: via `selenium` (dynamic content scraping)  
  - TRT Haber: via `requests + BeautifulSoup` (HTML parsing)

- **Preprocessing:**  
  - Text cleaning (punctuation, numbers, links, etc.)
  - Lemmatization using Zemberek-NLP
  - Turkish stopword removal
  - Filtering out very short (<3) and long (>30) tokens

- **Feature Extraction:**  
  - `TF-IDF` vectorization (`unigram + bigram`, `max_features=1000`)

- **Classification Algorithms:**
  - Naive Bayes
  - Logistic Regression
  - Decision Tree (J48)
  - Random Forest
  - Extra Trees (JRip alternative)
  - Support Vector Machine (SVM)
  - AdaBoostM1

- **Evaluation Methods:**
  - 70–30 Train/Test Split
  - 100% Train (for overfitting observation)
  - 5-Fold Cross-Validation
  - 10-Fold Cross-Validation

- **Evaluation Metrics:**
  - Accuracy
  - Precision
  - Recall
  - F1-Score

## Dataset

All records are merged in the `merged_dataset.csv` file with the following structure:

| source | text | label         |
|--------|------|---------------|
| trt    | ...  | non-sarcastic |
| zaytung| ...  | sarcastic     |


## Here is the results. For all the details of the project, you can open the file turkish-sarcasm-detection.pdf

![100_training_split](https://github.com/user-attachments/assets/82d7f74c-3252-4ec3-8297-484f8184df24)

![70-30_split](https://github.com/user-attachments/assets/8a8a2cf4-3605-4cab-bddb-c6ecfde5c685)

![5_fold_cross_validation](https://github.com/user-attachments/assets/efaea1bc-063d-40ba-94ff-94d5f4dc9760)

![10_fold_cross_validation](https://github.com/user-attachments/assets/69c8cda7-cd6f-46b7-8274-e6a7bbf0ac52)


# Data is collected from publicly available sources and intended for **academic use only**.
