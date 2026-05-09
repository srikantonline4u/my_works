"""Basic NLP demo: preprocessing, TF-IDF and a simple classifier.

Usage:
  pip install -r requirements.txt
  python nlp_basic.py "Some text to classify"

Or run without args to enter text interactively.
"""
import re
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def build_and_train():
    texts = [
        "The team won the championship after a thrilling game",
        "New breakthrough in AI improves model accuracy",
        "Government passed a new law affecting taxes",
        "The startup raised funding to expand its product",
        "The player scored a hat-trick in yesterday's match",
        "Researchers release a new paper on transformers",
        "Elections will be held next month across the country",
        "Company announced quarterly earnings beat expectations",
    ]
    labels = [
        'sports', 'tech', 'politics', 'business',
        'sports', 'tech', 'politics', 'business'
    ]
    texts = [preprocess(t) for t in texts]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=2000)
    X = vectorizer.fit_transform(texts)
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, labels)
    return vectorizer, clf


def predict(text: str, vectorizer: TfidfVectorizer, clf: LogisticRegression):
    t = preprocess(text)
    X = vectorizer.transform([t])
    pred = clf.predict(X)[0]
    probs = clf.predict_proba(X)[0]
    classes = clf.classes_
    return pred, dict(zip(classes, probs))


if __name__ == '__main__':
    vectorizer, clf = build_and_train()
    if len(sys.argv) > 1:
        input_text = ' '.join(sys.argv[1:])
    else:
        input_text = input('Enter text to classify: ')
    pred, probs = predict(input_text, vectorizer, clf)
    print(f"Input: {input_text}")
    print(f"Predicted label: {pred}")
    print('Class probabilities:')
    for k, v in sorted(probs.items(), key=lambda x: -x[1]):
        print(f" - {k}: {v:.3f}")
