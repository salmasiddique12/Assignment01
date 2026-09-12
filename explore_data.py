import pandas as pd

df = pd.read_csv("data/twcs.csv")
df["tweet_id"] = df["tweet_id"].astype(str)
df["response_tweet_id"] = df["response_tweet_id"].astype(str)
df["in_response_to_tweet_id"] = df["in_response_to_tweet_id"].astype(str)

print("Dataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# AmazonHelp customer tweets
amazon_customers = df[
    (df["inbound"] == True) &
    (df["text"].str.contains("@AmazonHelp", case=False, na=False))
]

print("\nAmazonHelp customer tweets:")
print("Count:", len(amazon_customers))


# AmazonHelp brand replies
amazon_replies = df[
    (df["inbound"] == False) &
    (df["author_id"] == "AmazonHelp")
]

print("\nAmazonHelp brand replies:")
print("Count:", len(amazon_replies))


# Connect customer tweets with brand replies
conversations = amazon_customers.merge(
    amazon_replies,
    left_on="response_tweet_id",
    right_on="tweet_id",
    suffixes=("_customer", "_brand")
)

print("\nReal AmazonHelp conversations:")
print("Total pairs:", len(conversations))

print(conversations[
    [
        "tweet_id_customer",
        "text_customer",
        "tweet_id_brand",
        "text_brand"
    ]
].head(100).to_excel(
    "amazon_conversations_sample.xlsx",
    index=False
))

print("\nConversation DataFrame:")

conversation_view = conversations[
    [
        "tweet_id_customer",
        "text_customer",
        "tweet_id_brand",
        "text_brand"
    ]
]

print(conversation_view.head(10).to_string(index=False))

conversation_view.head(100).to_excel(
    "amazon_conversations_sample.xlsx",
    index=False
)

print("Saved 100 conversations to amazon_conversations_sample.xlsx")

print("\nSample customer messages:")

print(
    conversation_view[
        ["text_customer"]
    ].sample(30, random_state=42).to_string(index=False)
)

# Create a clean dataset for the project

clean_conversations = conversations[
    [
        "tweet_id_customer",
        "text_customer",
        "tweet_id_brand",
        "text_brand"
    ]
].copy()

# Remove rows where customer message or brand reply is missing
clean_conversations = clean_conversations.dropna(
    subset=["text_customer", "text_brand"]
)

# Save the clean dataset
clean_conversations.to_csv(
    "data/amazonhelp_conversations.csv",
    index=False
)

print("\nClean dataset:")
print("Number of conversations:", len(clean_conversations))

print("\nColumns:")
print(clean_conversations.columns.tolist())

print("\nSample:")
print(clean_conversations.head(5).to_string(index=False))

print("\nSaved to: data/amazonhelp_conversations.csv")