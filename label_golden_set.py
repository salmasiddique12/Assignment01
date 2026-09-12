import pandas as pd

# Load golden set
df = pd.read_csv("data/golden_set.csv", dtype={"intent": "string"})

intents = [
    "order_delivery",
    "return_refund",
    "payment_billing",
    "account",
    "product_troubleshooting",
    "subscription",
    "product_availability",
    "customer_service",
    "other",
]

print("Golden Set Labeling Tool")
print("=" * 50)

for index, row in df.iterrows():

    # Skip already labelled rows
    if pd.notna(row["intent"]) and row["intent"] != "":
        continue

    print("\nCustomer message:")
    print("-" * 50)
    print(row["text_customer"])
    print("-" * 50)

    print("\nChoose an intent:")

    for number, intent in enumerate(intents, start=1):
        print(f"{number}. {intent}")

    while True:
        choice = input("\nEnter number (1-9): ")

        if choice.isdigit() and 1 <= int(choice) <= 9:
            selected_intent = intents[int(choice) - 1]
            break

        print("Please enter a number from 1 to 9.")

    df.at[index, "intent"] = selected_intent

    # Save after every label
    df.to_csv(
        "data/golden_set.csv",
        index=False
    )

    print(f"Saved: {selected_intent}")

print("\nAll 200 examples have been labelled!")