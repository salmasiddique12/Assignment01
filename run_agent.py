from pathlib import Path

import pandas as pd

from src.agent import (
    IntentClassifier,
    Retriever,
    escalation_decision,
    grounded_reply,
)


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent

golden_path = ROOT / "data" / "golden_set.csv"
full_path = ROOT / "data" / "amazonhelp_conversations.csv"


# --------------------------------------------------
# 2. Load golden set
# --------------------------------------------------

golden = pd.read_csv(
    golden_path,
    dtype={"intent": "string"}
)

# Keep only labelled examples
golden = golden[
    golden["intent"].notna()
    & (golden["intent"] != "")
].copy()

print("Labelled training examples:", len(golden))


# --------------------------------------------------
# 3. Load historical conversations
# --------------------------------------------------

if full_path.exists():
    corpus = pd.read_csv(full_path)
    print("Historical conversations:", len(corpus))
else:
    corpus = golden.copy()
    print("Full conversation file not found.")
    print("Using golden set as fallback.")


# --------------------------------------------------
# 4. Train intent classifier
# --------------------------------------------------

classifier = IntentClassifier()

classifier.train(
    golden["text_customer"],
    golden["intent"]
)


# --------------------------------------------------
# 5. Create historical retriever
# --------------------------------------------------

retriever = Retriever(corpus)


# --------------------------------------------------
# 6. Get customer message
# --------------------------------------------------

message = input("\nCustomer message: ").strip()


# --------------------------------------------------
# 7. Predict intent
# --------------------------------------------------

intent, confidence = classifier.predict(message)


# --------------------------------------------------
# 8. Retrieve historical evidence
# --------------------------------------------------

evidence = retriever.search(
    message,
    top_k=1
).iloc[0]


# --------------------------------------------------
# 9. Decide escalation
# --------------------------------------------------

escalate, reason = escalation_decision(
    message,
    confidence,
    evidence["similarity"]
)


# --------------------------------------------------
# 10. Generate grounded reply
# --------------------------------------------------

reply = grounded_reply(
    intent,
    message,
    evidence
)


# --------------------------------------------------
# 11. Display final agent output
# --------------------------------------------------

print("\n" + "=" * 60)
print("                AMAZON SUPPORT AGENT")
print("=" * 60)

print("\nCustomer message:")
print(message)

print("\nPredicted intent:")
print(intent)

print("\nConfidence:")
print(round(confidence, 3))

print("\nEscalate to human:")
print(escalate)

print("\nEscalation reason:")
print(reason)

print("\nDraft reply:")
print(reply)

print("\nHistorical evidence similarity:")
print(round(evidence["similarity"], 3))

print("\nHistorical customer example:")
print(evidence["text_customer"])

print("\nHistorical AmazonHelp response:")
print(evidence["text_brand"])

print("\n" + "=" * 60)
