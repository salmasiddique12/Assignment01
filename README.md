# 🤖 Hiver Support AI Agent

### AI-Powered Customer Support Agent | Hiver SDE Intern Take-Home Assignment

An end-to-end AI customer-support agent designed to assist support teams by **understanding customer intent, retrieving relevant historical conversations, drafting grounded responses, and determining when human intervention is required**.

This project was developed as part of the **Hiver SDE Intern Take-Home Assignment** using real-world customer-support conversation data.

---

## 👩‍💻 About the Project

Customer-support data is often messy, short, inconsistent, and full of spelling mistakes.

A useful support agent therefore needs to do more than simply generate text. It needs to:

* Understand what the customer is asking.
* Identify the likely support intent.
* Learn from how similar issues were handled historically.
* Produce a useful and grounded response.
* Recognize when it is uncertain.
* Escalate uncertain cases instead of confidently generating an incorrect answer.

This project focuses on building that complete workflow.

---

# 🎯 Objectives

The system is designed to perform three core tasks:

### 1. Intent Classification

Classify incoming customer messages into a small set of support intents derived from the dataset.

### 2. Historical Grounding

Retrieve similar historical customer-support conversations and use them as evidence when drafting a response.

### 3. Human Escalation

Estimate whether the system has enough confidence and evidence to handle the request automatically.

If confidence is too low, the system escalates the request to a human support agent.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   Customer Message  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Intent Classification│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Confidence Score   │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
              High Confidence       Low Confidence
                    │                     │
                    ▼                     ▼
          Historical Retrieval      Human Escalation
                    │
                    ▼
          Similar Conversations
                    │
                    ▼
             Evidence Context
                    │
                    ▼
             Drafted Response
                    │
                    ▼
             Support Decision
```

The architecture follows a simple principle:

> **Understand → Retrieve → Respond → Verify → Escalate when uncertain**

---

# 🔑 Key Features

## Intent Classification

The agent analyzes the incoming message and predicts the most likely support intent.

Example:

```text
Customer:
"I forgot my password"

Predicted Intent:
password_issue
```

The model also produces a confidence score.

This confidence is used downstream to determine whether automation is appropriate.

---

## 🔍 Historical Conversation Retrieval

The system searches historical customer-support conversations for similar examples.

The retrieved evidence contains:

* Historical customer message
* Historical support response
* Similarity score

Example:

```text
Customer Message:
"My password is not working"

Historical Customer Message:
"I can't log into my account"

Historical Support Response:
"Please contact support so we can help you regain access."
```

Historical conversations provide grounding for the generated response.

---

# 🧠 Confidence-Based Escalation

One of the key design decisions is **not to automatically answer every request**.

If the intent prediction has low confidence, the system escalates the request to a human.

Example:

```text
Predicted intent:
other

Confidence:
0.303

Escalate to human:
True

Escalation reason:
Low intent confidence
```

This reflects an important customer-support principle:

> **An uncertain answer is often worse than a human escalation.**

---

# 💬 Example

### Input

```text
my passwird is not workinh
```

The system processes the request through the complete pipeline.

### Output

```text
Predicted intent:
other

Confidence:
0.303

Escalate to human:
True

Escalation reason:
Low intent confidence

Draft reply:
I'm sorry you're having trouble. Please provide a few more details so Amazon support can better assist you.

Historical evidence similarity:
0.491
```

The typo-heavy input also demonstrates an important real-world challenge: customer messages are not always clean or grammatically correct.

---

# 📊 Dataset

The project is based on the **Customer Support on Twitter** dataset.

The original dataset contains approximately **3 million tweets** from customer-support interactions between customers and brands.

For development, a smaller sample is used rather than processing the entire dataset.

The current working pipeline processes approximately:

```text
81,664 historical conversations
```

A smaller labelled dataset is used for the initial intent-classification prototype.

---

# 🛠️ Technology Stack

| Technology   | Purpose                        |
| ------------ | ------------------------------ |
| Python       | Core programming language      |
| Pandas       | Data processing                |
| NumPy        | Numerical operations           |
| Scikit-learn | Machine learning               |
| Matplotlib   | Data visualization             |
| Excel/XLSX   | Dataset storage and inspection |
| Git          | Version control                |
| GitHub       | Source-code hosting            |

---

# 📁 Project Structure

```text
hiver-support-agent/
│
├── README.md
├── REPORT.md
│
├── run_agent.py
├── intents.py
├── create_golden_set.py
├── label_golden_set.py
├── explore_data.py
├── test_agent.py
│
├── amazon_conversations_sample.xlsx
│
├── data/
│   └── dataset files
│
└── src/
    └── agent implementation
```

---

# ⚙️ Installation

## Prerequisites

Recommended:

```text
Python 3.10+
Git
```

Check your Python installation:

```bash
python --version
```

---

## Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate into the project:

```bash
cd hiver-support-agent
```

---

## Create Virtual Environment

### Windows PowerShell

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

---

# 📦 Install Dependencies

If `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

Otherwise:

```bash
pip install pandas numpy scikit-learn matplotlib openpyxl
```

---

# ▶️ Run the Agent

From the project root:

```bash
python run_agent.py
```

The program will:

1. Load the labelled examples.
2. Load historical conversations.
3. Accept a customer message.
4. Predict the customer intent.
5. Calculate confidence.
6. Search historical conversations.
7. Draft a response.
8. Decide whether to escalate.

---

# 🧪 Testing

Run:

```bash
python test_agent.py
```

The testing workflow is intended to verify the main components of the support-agent pipeline.

---

# 📈 Evaluation Strategy

A production-quality support agent cannot be evaluated only by checking whether the code runs.

The intended evaluation framework includes:

### Intent Classification

* Accuracy
* Macro F1
* Precision
* Recall
* Per-intent performance
* Confusion matrix

### Escalation

* Escalation rate
* Correct escalation rate
* Incorrect auto-handling rate
* Performance at different confidence thresholds

### Response Quality

Responses should be evaluated on:

* Relevance
* Correctness
* Grounding
* Helpfulness
* Safety
* Clarity
* Appropriate escalation

---

# 🧪 Golden Evaluation Set

A robust evaluation requires a manually labelled evaluation set separate from the training examples.

The target is:

```text
150–250 manually labelled examples
```

The evaluation set should contain:

* Common intents
* Rare intents
* Ambiguous messages
* Short messages
* Long messages
* Typos
* Noisy customer language

The golden set should not be used for training.

This separation prevents data leakage and provides a more realistic estimate of generalization.

---

# 📊 Baselines

The final evaluation should compare the support agent against simple baselines.

### Baseline 1 — Majority Class

Always predict the most frequent intent.

This provides a trivial reference point.

### Baseline 2 — TF-IDF + Logistic Regression

A traditional machine-learning text classifier provides a stronger non-LLM baseline.

```text
Customer Message
       ↓
TF-IDF
       ↓
Logistic Regression
       ↓
Predicted Intent
```

The proposed system should be evaluated on the same golden set as both baselines.

---

# 🤖 LLM-as-Judge

Generated responses can be evaluated using an LLM-based judge with a fixed rubric.

Each response can be scored on a 1–5 scale for:

| Category    | Question                                        |
| ----------- | ----------------------------------------------- |
| Relevance   | Does the response address the customer's issue? |
| Correctness | Is the information accurate?                    |
| Grounding   | Is it supported by historical evidence?         |
| Helpfulness | Does it provide a useful next step?             |
| Safety      | Does it avoid unsafe automation?                |
| Clarity     | Is the response clear and professional?         |

The LLM judge should not automatically be treated as ground truth.

A human-labelled subset should be used to measure agreement.

---

# 🔎 Failure Analysis

Important failure modes observed during development include:

### 1. Misspelled Messages

Example:

```text
my passwird is not workinh
```

Noisy language can reduce classifier confidence.

### 2. Very Short Messages

Messages such as:

```text
"It doesn't work"
```

contain insufficient context.

### 3. Overlapping Intents

Different support issues may contain similar words and concepts.

### 4. Limited Labelled Data

A small number of labelled examples limits the model's ability to generalize to unseen phrasing.

### 5. Missing Historical Evidence

The system may not find a sufficiently similar historical conversation for unusual requests.

---

# ⚠️ Current Limitations

This implementation is currently a **working prototype** rather than a production-ready customer-support system.

Current limitations include:

* Small labelled training set.
* Limited intent taxonomy.
* Evaluation framework still requires expansion.
* Historical data is a sampled subset.
* Retrieval quality depends on available historical conversations.
* Customer messages can be ambiguous or misspelled.
* Historical support responses may contain inconsistencies.
* The agent does not directly perform account-level actions.
* Automated responses should not be treated as guaranteed correct.

These limitations are important because a high model confidence score does not necessarily mean that a response is safe or correct.

---

# 🚀 Future Improvements

With additional development time, I would focus on:

### Better Intent Classification

Expand and balance the labelled training data.

### Better Retrieval

Use stronger semantic embeddings and reranking to improve historical evidence retrieval.

### Confidence Calibration

Tune escalation thresholds using validation data rather than selecting them arbitrarily.

### Conversation-Level Context

Use the entire conversation thread rather than relying only on individual messages.

### Stronger Evaluation

Build the complete 150–250 example golden set and compare the system against multiple baselines.

### Human Evaluation

Measure how closely the LLM judge agrees with human reviewers.

### Production Safety

Introduce explicit rules for sensitive operations such as:

* Payments
* Refunds
* Account recovery
* Authentication
* Personal information
* Account changes

These should receive additional verification or human review.

---

# 📝 Engineering Decisions

Some important design decisions include:

1. Use a small intent taxonomy rather than attempting to classify every possible support issue.
2. Use historical conversations as grounding evidence.
3. Keep evaluation data separate from training data.
4. Use confidence-based escalation.
5. Prefer human review for uncertain cases.
6. Include noisy customer messages in evaluation.
7. Compare against simple baselines.
8. Evaluate response quality separately from classification quality.
9. Treat LLM-as-judge results as evaluation evidence rather than absolute truth.
10. Use a dataset sample to keep development reproducible.
11. Avoid directly executing sensitive customer actions.
12. Report failure cases rather than hiding them.
13. Focus on evidence and evaluation rather than relying on a single accuracy number.

---

# 📌 What Is Misleading About a Headline Number?

A single accuracy number can be misleading.

For example:

```text
90% Accuracy
```

does not necessarily mean:

```text
90% of customers receive good automated support.
```

A classifier may perform well on common intents while failing on rare but important customer problems.

Similarly:

```text
High classification accuracy
        ≠
High-quality support
```

A trustworthy support agent must also retrieve relevant evidence, generate grounded responses, identify uncertainty, and escalate appropriately.

Therefore, performance should be considered using multiple signals:

```text
Intent Quality
+
Retrieval Quality
+
Response Quality
+
Escalation Quality
+
Failure Analysis
```

---

# 📚 Reproducibility

The project is designed so that a reviewer can reproduce the core pipeline quickly.

Basic workflow:

```bash
git clone <repository-url>
cd hiver-support-agent

python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

python run_agent.py
```

The development dataset is intentionally smaller than the original dataset so that the project can be tested without processing millions of tweets.

---

# 🔐 Security

Do not commit sensitive information to the repository.

The `.gitignore` should include:

```text
.venv/
__pycache__/
*.pyc
.env
```

API keys, credentials, tokens, and private customer information should never be committed to GitHub.

---

# 📄 Assignment Report

Additional project details and analysis are available in:

```text
REPORT.md
```

---

# 👩‍💻 Author

**Salma**

AI / Machine Learning Developer

Interested in building practical AI systems that combine:

```text
Machine Learning
+
Natural Language Processing
+
Generative AI
+
Software Engineering
```

This project represents hands-on work in building an AI system from real-world, noisy customer-support data rather than relying only on theoretical ML examples.

---

# ⭐ Key Takeaway

The objective of this project is not simply to generate a convincing support response.

The goal is to build a system that knows:

> **what it understands, what evidence it has, and when it should ask a human for help.**

That distinction is central to building reliable AI systems for real-world customer support.
