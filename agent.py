import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

## text clean kr rhe h

def clean_text(text):
    """
    Basic text cleaning.
    """
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()

## simple ML baseline/working classifier
class IntentClassifier:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=2
        )

        self.model = LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )

    def train(self, texts, labels):
        """
        Train classifier using labelled examples.
        """

        texts = [clean_text(text) for text in texts]

        X = self.vectorizer.fit_transform(texts)

        self.model.fit(X, labels)

    def predict(self, text):
        """
        Predict intent and confidence.
        """

        text = clean_text(text)

        X = self.vectorizer.transform([text])

        prediction = self.model.predict(X)[0]

        probabilities = self.model.predict_proba(X)[0]

        confidence = probabilities.max()

        return prediction, confidence


class Retriever:

    def __init__(self, conversations):
        """
        conversations = historical AmazonHelp conversations
        """

        self.conversations = conversations.copy()

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=2
        )

        self.matrix = self.vectorizer.fit_transform(
            self.conversations["text_customer"].fillna("").map(clean_text)
        )

    def search(self, query, top_k=3):
        """
        Find the most similar historical customer messages.
        """

        query = clean_text(query)

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.matrix
        )[0]

        top_indices = scores.argsort()[-top_k:][::-1]

        results = self.conversations.iloc[top_indices].copy()

        results["similarity"] = scores[top_indices]

        return results


def escalation_decision(message, confidence, similarity):
    """
    Decide whether the conversation should go to a human.
    """

    message = clean_text(message)

    # Low confidence means the classifier is unsure
    if confidence < 0.50:
        return True, "Low intent confidence"

    # Weak historical evidence
    if similarity < 0.18:
        return True, "No strong historical evidence"

    # Sensitive or potentially risky issues
    risky_words = [
        "hack",
        "hacked",
        "fraud",
        "stolen",
        "unauthorized",
        "security",
        "password",
    ]

    if any(word in message for word in risky_words):
        return True, "Potential security or sensitive issue"

    return False, "High confidence with relevant historical evidence"


def grounded_reply(intent, message, evidence):
    """
    Generate a conservative reply based on historical AmazonHelp behaviour.
    """

    historical_reply = evidence["text_brand"]

    if intent == "order_delivery":
        return (
            "I'm sorry your order hasn't arrived yet. "
            "Please check the latest delivery/tracking information for your order. "
            "If it is still delayed, please contact Amazon support with your order details."
        )

    if intent == "return_refund":
        return (
            "I'm sorry you're having trouble with your return or refund. "
            "Please provide your order details so the support team can check the issue."
        )

    if intent == "payment_billing":
        return (
            "Sorry about the payment or billing issue. "
            "Please provide the relevant order or payment details so the support team can investigate."
        )

    if intent == "account":
        return (
            "Sorry you're having trouble with your account. "
            "Please contact Amazon support so they can securely verify and assist with your account."
        )

    if intent == "product_troubleshooting":
        return (
            "Sorry you're having trouble with the product. "
            "Please share the product/device details and the issue you're experiencing so support can help troubleshoot it."
        )

    if intent == "subscription":
        return (
            "Sorry you're having trouble with your subscription. "
            "Please provide your account or subscription details so support can check this for you."
        )

    if intent == "product_availability":
        return (
            "Sorry the product isn't currently available. "
            "Please check the product page for the latest availability information."
        )

    if intent == "customer_service":
        return (
            "I'm sorry you haven't received the help you expected. "
            "Please provide your details so the support team can look into the issue."
        )

    return (
        "I'm sorry you're having trouble. "
        "Please provide a few more details so Amazon support can better assist you."
    )