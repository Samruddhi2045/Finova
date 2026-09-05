from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .services.controller import controller
from .services.data_store import store
from .services.investigator import investigator
from .services.evaluation import evaluate
from .services.copilot import answer_copilot

app = FastAPI(title="Finova — AI Finance Decision Support & Control Platform", version="1.0.0")
ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")

@app.on_event("startup")
def startup():
    store.init()
    if not store.has_data():
        controller.generate_and_run()

@app.get("/")
def index(): return FileResponse(FRONTEND / "index.html")
@app.get("/api/dashboard")
def dashboard(): return controller.dashboard()
@app.post("/api/reconciliation/run")
def run_reconciliation(): return controller.run()
@app.get("/api/exceptions")
def exceptions(): return store.exceptions()
@app.get("/api/exceptions/{eid}")
def exception_detail(eid: str):
    x = store.exception(eid)
    if not x: raise HTTPException(404, "Exception not found")
    return x
@app.post("/api/exceptions/{eid}/investigate")
def investigate(eid: str):
    x = store.exception(eid)
    if not x: raise HTTPException(404, "Exception not found")
    return investigator.investigate(x)
@app.get("/api/exceptions/{eid}/similar")
def similar(eid: str):
    x = store.exception(eid)
    if not x: raise HTTPException(404, "Exception not found")
    return investigator.similar(x)
@app.get("/api/evaluation")
def evaluation(): return evaluate(store.records(), store.ground_truth(), store.exceptions())
@app.get("/api/audit")
def audit(): return store.audit()
@app.get("/api/policies")
def policies(): return store.policies()
@app.get("/api/health")
def health(): return {"status":"healthy","ai_mode":investigator.mode}
@app.post("/api/copilot")
def copilot(payload: dict): return answer_copilot(payload.get("question", ""), store)
@app.post("/api/reviews/{eid}/decision")
def review(eid: str, payload: dict):
    if not store.exception(eid):
        raise HTTPException(404, "Exception not found")
    decision = payload.get("decision")
    if decision not in {"APPROVE","REJECT","ESCALATE","REQUEST_INFO","RESOLVE"}: raise HTTPException(400,"Invalid decision")
    return store.review(eid, decision, payload.get("note", ""))
