def answer_copilot(q, store):
    q=q.lower(); d=__import__('app.services.controller',fromlist=['controller']).controller.dashboard(); ex=store.exceptions()
    if 'match' in q: return {'answer':f"Current reconciliation match rate is {d['match_rate']}% across {d['total_records']:,} records."}
    if 'high' in q or 'risk' in q: return {'answer':f"There are {d['high_risk']} high/critical-risk exceptions with total financial exposure of ₹{d['financial_exposure']:,.2f}."}
    if 'unresolved' in q or 'exception' in q: return {'answer':f"There are {d['unresolved']} unresolved exceptions. The largest current exception is {max(ex,key=lambda x:x['discrepancy_amount'])['exception_id']} with ₹{max(ex,key=lambda x:x['discrepancy_amount'])['discrepancy_amount']:,.2f} discrepancy."}
    return {'answer':'I can answer questions about match rate, unresolved exceptions, high-risk exposure, exception counts, and reconciliation health using Finova data.'}
