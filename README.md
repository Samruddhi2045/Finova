# FINOVA : AI Finance Decision Support & Control Platform

**AI investigates. Finance decides.**

Finova is a finance support platform designed to make reconciliation easier and faster. It checks payment, settlement, invoice, and bank records, finds mismatches, explains possible reasons, and helps finance teams decide what to do next.

## What Finova Does

* Works with 5,000 synthetic financial records
* Compares payments, settlements, invoices, and bank records
* Automatically identifies mismatches and exceptions
* Calculates financial impact and risk
* Uses AI to investigate and explain exceptions
* Finds similar cases from previous exceptions
* Helps finance teams review and resolve issues
* Keeps track of important actions through an audit trail
* Includes a Finance Copilot for quick data-based questions
* Provides policies to control when human review is needed
* Shows real evaluation results such as Precision, Recall, and F1-score
* Works even without an external AI API using a built-in fallback
* Uses FastAPI, SQLite, and a browser-based frontend

## How It Works

**Financial Records -> Reconciliation -> Exception Detection -> AI Investigation -> Risk Analysis -> Human Review -> Audit Trail**

The main idea is simple: **AI helps investigate the problem, but the final financial decision stays with the finance professional.**

## Running Finova

### 1. Go to the backend folder

```bash
cd backend
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

Finova automatically creates its SQLite database and loads the demo dataset when no records are available.

To run reconciliation again:

```bash
curl -X POST http://127.0.0.1:8000/api/reconciliation/run
```

## Testing

With the application running, run:

```bash
python -m unittest discover -s tests
```

The tests check the main API, evaluation results, dashboard data, and exception queue.

No external AI API is required for the default demo.

## Architecture

Finova follows a simple approach:

**Deterministic Financial Truth → AI Investigation → Policy & Human Control → Audit Trail**

The financial calculations and reconciliation results are handled using deterministic logic. AI is mainly used to explain issues, find patterns, and suggest possible next steps.

AI cannot:

* Move money
* Change financial balances
* Delete financial records
* Approve payments
* Bypass finance policies

## Demo Flow

A simple way to demonstrate Finova is:

1. **Overview** - Show the reconciliation status, match rate, exceptions, and financial exposure.
2. **Exceptions** - Select an exception that needs attention.
3. **AI Investigation** - See what happened, the possible reason, and supporting evidence.
4. **Exception Memory** - Compare it with similar past cases.
5. **Review Desk** - Approve, reject, resolve, or escalate the case.
6. **Audit Trail** - Show the actions taken and decisions made.
7. **Evaluation** - Show the actual Precision, Recall, F1-score, and other results.
8. **Finance Copilot** - Ask questions such as *“What is our current match rate?”*

## Why Finova?

Finance teams often spend a lot of time checking records manually and investigating small mismatches.

Finova brings these steps together in one place so that finance professionals can focus on the cases that actually need their attention.

**AI investigates. Finance decides.**
