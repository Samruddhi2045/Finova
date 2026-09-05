# FINOVA — AI Finance Decision Support & Control Platform

**AI investigates. Finance decides.**

Finova is a controller-style finance operations platform for reconciliation, exception investigation, risk prioritization, policy-controlled recommendations, human review, auditability, and measurable evaluation.

## What is implemented
- 5,000 deterministic synthetic payment/settlement/invoice/bank records
- Controlled exception taxonomy and seeded ground truth
- Deterministic reconciliation + discrepancy calculations
- Financial exposure and transparent risk scoring
- AI Investigation interface with deterministic fallback
- Exception Memory via historical similarity retrieval
- Human Review Desk with audit events
- Finance Copilot grounded in application data
- Policy engine
- Evaluation endpoint and dashboard with live precision, recall, F1, and confusion counts
- FastAPI backend + browser frontend + SQLite persistence
- No secrets required for the default demo

## Run
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

The default startup path initializes the SQLite database and seeds the deterministic
5,000-record dataset when no records exist. To force a fresh reconciliation run,
use the Reconciliation page or:

```bash
curl -X POST http://127.0.0.1:8000/api/reconciliation/run
```

## Verification

With the API running, execute the included smoke tests:

```bash
python -m unittest discover -s tests
```

The tests verify health, evaluation, and consistency between the dashboard and
exception queue. The application does not require an external AI provider for
the default deterministic fallback mode.

## Architecture
Deterministic Financial Truth → AI Investigation → Policy & Human Control → Audit Trail.

The AI layer can explain and recommend, but it cannot move money, modify balances, delete records, or bypass policy.

## Demo flow
1. Overview → show match rate, unresolved queue and financial exposure.
2. Exceptions → investigate a high-risk discrepancy.
3. Exception Memory → show similar historical cases.
4. Review Desk → resolve or escalate with human decision.
5. Audit Trail → show the decision event.
6. Evaluation → show metrics computed from seeded ground truth.
7. Finance Copilot → ask “What is our current match rate?”
