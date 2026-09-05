import random, uuid
from .data_store import store
class Controller:
    def generate_and_run(self):
        records=[]; truth={}; exceptions=[]; random.seed(42)
        types=['EXACT_MATCH','AMOUNT_MISMATCH','MISSING_SETTLEMENT','FEE_DISCREPANCY','DUPLICATE_PAYMENT','TIMING_DIFFERENCE','PARTIAL_SETTLEMENT','HIGH_VALUE_EXCEPTION','TAX_DISCREPANCY']
        for i in range(1,5001):
            tid=f'TXN-{i:06d}'; amt=random.randint(200,100000); t=random.choice(types) if i<=900 else 'EXACT_MATCH'
            payment=amt; settlement=amt; fee=round(amt*.018,2); tax=round(fee*.18,2); status='SETTLED'
            if t=='AMOUNT_MISMATCH': settlement=amt-random.choice([25,75,250,1250])
            elif t=='MISSING_SETTLEMENT': settlement=0; status='MISSING'
            elif t=='FEE_DISCREPANCY': fee=round(amt*.024,2)
            elif t=='DUPLICATE_PAYMENT': payment=amt*2
            elif t=='TIMING_DIFFERENCE': status='LATE'
            elif t=='PARTIAL_SETTLEMENT': settlement=round(amt*.72,2)
            elif t=='HIGH_VALUE_EXCEPTION': amt=random.randint(150000,500000); payment=amt; settlement=amt-random.randint(10000,30000)
            elif t=='TAX_DISCREPANCY': tax=round(fee*.28,2)
            r={'transaction_id':tid,'customer_id':f'C-{random.randint(100,999)}','order_id':f'O-{i:06d}','payment_amount':payment,'currency':'INR','payment_method':random.choice(['UPI','CARD','NETBANKING']),'payment_timestamp':f'2026-09-{random.randint(1,5):02d}','settlement_id':f'S-{i:06d}','settlement_amount':settlement,'settlement_date':f'2026-09-{random.randint(2,7):02d}','fee':fee,'tax':tax,'invoice_amount':amt,'bank_credited_amount':settlement,'status':status}
            records.append(r); truth[tid]={'type':t,'has_exception':t!='EXACT_MATCH'}
            if t!='EXACT_MATCH':
                disc=abs(payment-settlement); score=min(100,round(disc/max(payment,1)*45 + (25 if t in ('HIGH_VALUE_EXCEPTION','DUPLICATE_PAYMENT') else 0) + (20 if disc>10000 else 0),1))
                risk='CRITICAL' if score>=81 else 'HIGH' if score>=61 else 'MEDIUM' if score>=31 else 'LOW'
                exceptions.append({'exception_id':f'EXC-{i:06d}','transaction_id':tid,'exception_type':t,'discrepancy_amount':disc,'risk_score':score,'risk_level':risk,'root_cause':'Settlement difference requiring evidence review','recommended_action':'Review supporting settlement evidence','review_status':'PENDING','evidence':{'payment_amount':payment,'settlement_amount':settlement,'fee':fee,'tax':tax,'invoice_amount':amt}})
        store.replace(records,exceptions,truth)
        return {'records':len(records),'exceptions':len(exceptions)}
    def run(self): return self.generate_and_run()
    def dashboard(self):
        r=store.records(); e=store.exceptions(); matched=len(r)-len(e); exposure=sum(x['discrepancy_amount'] for x in e); high=sum(1 for x in e if x['risk_level'] in ('HIGH','CRITICAL'))
        return {'total_records':len(r),'matched':matched,'unmatched':len(e),'match_rate':round(matched/len(r)*100,2) if r else 0,'unresolved':sum(x.get('review_status')=='PENDING' for x in e),'financial_exposure':round(exposure,2),'high_risk':high,'exception_types':self._counts(e)}
    def _counts(self,e):
        d={}
        for x in e:d[x['exception_type']]=d.get(x['exception_type'],0)+1
        return d
controller=Controller()
