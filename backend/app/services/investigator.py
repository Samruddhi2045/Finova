import os
from .data_store import store
class Investigator:
    mode='deterministic-fallback'
    def similar(self,x):
        ex=store.exceptions(); same=[y for y in ex if y['exception_type']==x['exception_type'] and y['exception_id']!=x['exception_id']]
        return [{'exception_id':y['exception_id'],'transaction_id':y['transaction_id'],'root_cause':y['root_cause'],'discrepancy_amount':y['discrepancy_amount']} for y in same[:3]]
    def investigate(self,x):
        d=x['discrepancy_amount']; typ=x['exception_type']; evidence=x['evidence'];
        cause={'FEE_DISCREPANCY':'Settlement fee differs from the expected fee calculation','TAX_DISCREPANCY':'Tax treatment differs from the expected tax basis','DUPLICATE_PAYMENT':'Payment amount suggests duplicate/duplicate-like activity','MISSING_SETTLEMENT':'Payment exists but settlement evidence is missing','TIMING_DIFFERENCE':'Settlement status indicates a timing-related exception','PARTIAL_SETTLEMENT':'Settlement is materially below the payment value','HIGH_VALUE_EXCEPTION':'High-value discrepancy increases financial exposure','AMOUNT_MISMATCH':'Settlement amount differs from payment amount'}.get(typ,'Transaction requires reconciliation review')
        action='Escalate for controller review' if x['risk_level'] in ('HIGH','CRITICAL') else 'Review settlement evidence and resolve if supported'
        return {'summary':f'{typ.replace("_"," ").title()} detected with ₹{d:,.2f} discrepancy.','exception_type':typ,'probable_root_cause':cause,'evidence':evidence,'similar_cases':self.similar(x),'risk_level':x['risk_level'],'risk_score':x['risk_score'],'recommended_action':action,'confidence':0.91 if typ!='HIGH_VALUE_EXCEPTION' else 0.96,'requires_human_review':x['risk_level'] in ('HIGH','CRITICAL') or typ=='DUPLICATE_PAYMENT'}
investigator=Investigator()
