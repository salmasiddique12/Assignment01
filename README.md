# Assignment01
# Hiver Support AI Agent

An AI-powered customer support agent built for the **Hiver SDE Intern Take-Home Assignment**.

The system analyzes customer-support conversations, classifies incoming messages into support intents, retrieves historically similar conversations, drafts a brand-grounded response, and decides whether the request should be automatically handled or escalated to a human.

---

## 1. Problem

Customer-support conversations are noisy, short, typo-heavy, and often lack context.

The goal of this project is to build a support agent that can:

1. Classify incoming customer messages into a small set of intents.
2. Draft replies grounded in historically similar customer-support conversations.
3. Decide whether a message can be auto-handled or should be escalated to a human.
4. Provide measurable evidence that the system works.

The system is designed around the following pipeline:

```text
Customer Message
       |
       v
Intent Classification
       |
       v
Confidence Check
       |
       +-------- Low Confidence --------> Human Escalation
       |
       v
Historical Conversation Retrieval
       |
       v
Grounded Reply Draft
       |
       v
Final Support Decision
```

---

## 2. Dataset

The primary dataset is **Customer Support on Twitter** from Kaggle:

`thoughtvector/customer-support-on-twitter`

The original dataset contains approximately 3 million tweets from customer-support conversations between customers and brands.

For this project, a smaller subsample is used for development and evaluation so that the complete pipeline can be reproduced quickly.

### Data used by this project

* Historical customer-support conversations
* A selected brand/support account
* Hand-labelled examples for intent classification
* A separate golden evaluation set

The project does not require running against the full dataset.

---

## 3. Project Structure

```text
hiver-support-agent/
│
├── README.md
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
│   └── project data
│
└── src/
    └── agent implementation
```

---

## 4. Main Components

### Intent Classification

The classifier maps an incoming customer message to one of the project-specific support intents.

Example:

```text
Customer:
"I forgot my password"

Intent:
password_issue
```

The classifier also returns a confidence score.

Low-confidence predictions are not blindly automated.

---

### Historical Retrieval

The agent searches historical support conversations for examples that are semantically similar to the current customer message.

The retrieved conversation provides evidence about how similar issues were handled historically.

Example:

```text
Customer message:
"My password is not working"

Historical example:
"I can't log into my account"

Historical response:
"Please contact support so we can help you regain access."
```

The historical response is used as grounding/context rather than treating the model's generated answer as authoritative.

---

### Escalation

The system decides whether a request should be automatically handled or sent to a human.

Current escalation signals include:

* Low intent confidence
* Unclear customer request
* Insufficient historical evidence
* Potentially unsupported situations

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

This conservative behaviour is intentional: an uncertain support agent should prefer escalation over confidently giving an incorrect answer.

---

## 5. Running the Project

### Requirements

Python 3.10+ is recommended.

Install dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install the main dependencies:

```bash
pip install pandas numpy scikit-learn matplotlib openpyxl
```

---

### Run the Agent

From the project root:

```bash
python run_agent.py
```

Example:

```text
Customer message: my password is not working

============================================================
                SUPPORT AGENT
============================================================

Predicted intent:
password_issue

Confidence:
0.XX

Escalate to human:
...

Escalation reason:
...

Draft reply:
...

Historical evidence similarity:
...

Historical customer example:
...

Historical support response:
...
```

---

## 6. Creating the Golden Evaluation Set

The golden set contains manually labelled customer messages that are kept separate from the training data.

Generate candidate examples:

```bash
python create_golden_set.py
```

The target evaluation set contains approximately **150–250 examples**, as required by the assignment.

Each example should contain at least:

```text
customer_message
gold_intent
```

Additional fields may include:

```text
predicted_intent
confidence
escalation_decision
```

### Sampling methodology

Examples should be sampled from real customer-support conversations rather than generated artificially.

The sample should include:

* Common support issues
* Rare intents
* Short messages
* Long messages
* Misspellings
* Ambiguous requests
* Different ways of expressing the same problem

The examples are manually labelled using the project's intent definitions.

---

## 7. Evaluation

The evaluation harness measures both classification quality and support-agent behaviour.

Recommended metrics include:

### Intent Classification

* Accuracy
* Macro F1
* Per-intent precision
* Per-intent recall
* Confusion matrix

Macro F1 is particularly important because some support intents may have fewer examples than others.

### Escalation

Measure:

* Percentage of requests escalated
* Escalation precision
* Escalation recall
* Incorrect auto-handling rate

The goal is not simply to minimize escalation.

A useful support agent should balance automation with safety.

### Reply Quality

Generated replies are evaluated for:

1. Relevance
2. Correctness
3. Grounding in historical evidence
4. Helpfulness
5. Appropriate escalation
6. Hallucination/unsupported claims
7. Professional tone

---

## 8. Baselines

The AI agent is compared against at least two simpler approaches.

### Baseline 1 — Majority Class

Always predict the most frequent intent in the training set.

This establishes a trivial lower bound.

### Baseline 2 — Simple Text Classifier

A simple TF-IDF + Logistic Regression classifier is used as a stronger non-LLM baseline.

```text
Customer Message
       |
       v
TF-IDF
       |
       v
Logistic Regression
       |
       v
Intent
```

The final system should be compared against both baselines on the same golden set.

---

## 9. LLM-as-Judge

An LLM-based evaluator can score generated support replies using a fixed rubric.

Each response is evaluated on a 1–5 scale for:

| Criterion   | Description                                  |
| ----------- | -------------------------------------------- |
| Relevance   | Addresses the customer's actual problem      |
| Correctness | Does not introduce unsupported information   |
| Grounding   | Consistent with historical support behaviour |
| Helpfulness | Provides a useful next step                  |
| Safety      | Escalates when appropriate                   |
| Clarity     | Clear and professional                       |

The judge should receive the customer message, historical evidence, generated response, and evaluation rubric.

---

## 10. Human Agreement

LLM-as-judge results should not be treated as ground truth.

A subset of generated replies is manually evaluated using the same rubric.

Agreement between human and LLM ratings can then be measured using:

* Exact agreement
* Mean absolute difference
* Correlation
* Cohen's kappa for categorical judgements where applicable

This provides evidence for how reliable the automated judge is.

---

## 11. Failure Analysis

The evaluation should identify the top failure modes rather than reporting only one headline metric.

Examples of failure categories include:

### 1. Short or ambiguous messages

Example:

```text
"it doesn't work"
```

There may not be enough information to identify the customer's intent.

### 2. Misspellings

Example:

```text
"my passwird is not workinh"
```

Noisy text can reduce classifier confidence.

### 3. Overlapping intents

Different support issues may use similar vocabulary, making intent boundaries difficult.

### 4. Insufficient historical evidence

A relevant historical conversation may not exist in the retrieved sample.

### 5. Incorrect automation

A high-confidence prediction does not necessarily mean that automatic handling is safe.

These failures should be supported with actual examples from the evaluation set.

---

## 12. What Is Misleading About My Headline Number?

A high classification accuracy alone does not mean the support agent is trustworthy.

For example, if one intent is much more common than others, a classifier can achieve a deceptively high accuracy by predicting common intents while performing poorly on rare but important cases.

Similarly:

```text
High intent accuracy
        ≠
High-quality support
```

A useful support agent must also:

* Retrieve relevant evidence
* Produce a grounded response
* Avoid hallucinating policies
* Escalate uncertain cases
* Handle noisy customer messages
* Perform well across different intents

Therefore, headline accuracy should always be interpreted together with macro F1, per-intent results, reply quality, escalation behaviour, and failure analysis.

---

## 13. Design Decisions

Important non-obvious decisions made during development include:

1. Use a small intent taxonomy rather than attempting to reproduce every possible customer issue.
2. Use manually labelled examples for evaluation rather than relying only on training metrics.
3. Keep the golden set separate from training examples.
4. Use historical conversations as grounding evidence.
5. Include confidence-based escalation.
6. Prefer human escalation when intent confidence is low.
7. Include noisy and misspelled customer messages in evaluation.
8. Compare against simple baselines.
9. Evaluate generated replies separately from intent classification.
10. Treat LLM-as-judge as an evaluator rather than ground truth.
11. Measure human/LLM agreement.
12. Report failure cases instead of hiding them.
13. Use a subsample of the large dataset for reproducibility.
14. Avoid claiming that a generated response is correct solely because it sounds fluent.
15. Prefer conservative automation for uncertain support cases.

---

## 14. Limitations

This is a prototype built for the take-home assignment.

Important limitations include:

* The labelled training set is relatively small.
* The historical dataset is a subsample rather than the full Twitter support dataset.
* Historical responses may themselves contain inconsistencies.
* Retrieval quality depends on the available historical examples.
* Intent boundaries can be subjective.
* LLM-based evaluation can introduce evaluator bias.
* The system does not have access to real customer account information.
* The system should therefore draft responses rather than directly execute account actions.

---

## 15. Future Improvements

With another week of development, I would focus on:

### Better Intent Classification

Increase the labelled training set and improve handling of noisy/typo-heavy messages.

### Better Retrieval

Use stronger semantic retrieval and reranking to identify the most relevant historical support conversations.

### Confidence Calibration

Calibrate confidence scores so that escalation thresholds correspond more reliably to actual error rates.

### Better Reply Evaluation

Expand the human-labelled evaluation set and improve validation of the LLM judge.

### Conversation Context

Use multiple messages from the same conversation rather than relying primarily on an isolated customer message.

### Production Safety

Add explicit policies for:

* Sensitive requests
* Account actions
* Refunds
* Payments
* Authentication
* Personal information

These should be routed to humans where appropriate.

---

## 16. Example

Input:

```text
my passwird is not workinh
```

The agent processes the message through:

```text
                    Customer Message
                           |
                           v
                 Intent Classification
                           |
                           v
                  Confidence = 0.XXX
                           |
             +-------------+-------------+
             |                           |
        High confidence             Low confidence
             |                           |
             v                           v
       Historical Search           Human Escalation
             |
             v
       Similar Conversation
             |
             v
        Grounded Draft Reply
```

This architecture is intentionally conservative: the system should not automate a request simply because it can generate a fluent answer.

---

## 17. Reproducibility

The goal is to make the main results reproducible in under 15 minutes using a sampled dataset.

Basic setup:

```bash
git clone <repository-url>
cd hiver-support-agent

python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

python run_agent.py
```

Evaluation:

```bash
python create_golden_set.py
python test_agent.py
```

If evaluation scripts require API credentials, configure them through environment variables rather than committing credentials to GitHub.

---

## 18. Conclusion

This project focuses on building a support agent that is not only capable of generating responses, but also provides evidence for when those responses should be trusted.

The central design principle is:

```text
Classify
   ↓
Retrieve evidence
   ↓
Draft response
   ↓
Evaluate confidence
   ↓
Automate OR Escalate
```

The system is intentionally designed around **measurable performance and conservative escalation**, rather than treating fluent text generation as proof of correctness.
