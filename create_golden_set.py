import pandas as pd

# Load our clean AmazonHelp conversations
df = pd.read_csv("data/amazonhelp_conversations.csv")

# Randomly select 200 conversations
golden = df.sample(
    n=200,
    random_state=42
).copy()

# Add an empty column for our manual labels
golden["intent"] = ""

# Save the golden set
golden.to_csv(
    "data/golden_set.csv",
    index=False
)

print("Golden set created!")
print("Number of examples:", len(golden))
print("Saved to: data/golden_set.csv")

