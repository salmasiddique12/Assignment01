from collections import Counter
import re

texts = conversation_view["text_customer"].dropna()

words = []

for text in texts:
    words.extend(
        re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    )

word_counts = Counter(words)

print("\nMost common customer words:")
print(word_counts.most_common(30))

## step2
INTENTS = [
    "order_delivery",
    "return_refund",
    "payment_billing",
    "account",
    "product_troubleshooting",
    "subscription",
    "customer_service",
    "other",
]

