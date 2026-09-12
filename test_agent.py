import pandas as pd

from src.agent import IntentClassifier, Retriever


# Load AmazonHelp historical conversations
df = pd.read_csv(
    "data/amazonhelp_conversations.csv"
)

print("Loaded conversations:", len(df))


# -------------------------
# 1. Train intent classifier
# -------------------------

# Golden set contains our human labels
golden = pd.read_csv(
    "data/golden_set.csv",
    dtype={"intent": "string"}
)

# Keep only labelled examples
golden = golden[
    golden["intent"].notna()
    & (golden["intent"] != "")
]

print("Labelled examples:", len(golden))


classifier = IntentClassifier()

classifier.train(
    golden["text_customer"],
    golden["intent"]
)


# -------------------------
# 2. Create retriever
# -------------------------

retriever = Retriever(df)


# -------------------------
# 3. Test customer message
# -------------------------

message = "My order has not arrived yet"

intent, confidence = classifier.predict(message)

print("\nCustomer message:")
print(message)

print("\nPredicted intent:")
print(intent)

print("\nConfidence:")
print(round(confidence, 3))


# -------------------------
# 4. Retrieve evidence
# -------------------------

results = retriever.search(
    message,
    top_k=3
)

print("\nSimilar historical conversations:")
print("=" * 60)

for _, row in results.iterrows():

    print("\nCustomer:")
    print(row["text_customer"])

    print("\nAmazonHelp:")
    print(row["text_brand"])

    print("\nSimilarity:")
    print(round(row["similarity"], 3))
    