import json, sqlite3
from pathlib import Path
DB = Path(__file__).resolve().parents[3] / 'data' / 'finova.db'
class Store:
    def conn(self):
        DB.parent.mkdir(exist_ok=True)
        c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
    def init(self):
        c=self.conn(); c.executescript('''CREATE TABLE IF NOT EXISTS records(id TEXT PRIMARY KEY, data TEXT, truth TEXT); CREATE TABLE IF NOT EXISTS exceptions(id TEXT PRIMARY KEY, data TEXT); CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT, event TEXT, detail TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP); CREATE TABLE IF NOT EXISTS reviews(id INTEGER PRIMARY KEY AUTOINCREMENT, exception_id TEXT, decision TEXT, note TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP);'''); c.commit(); c.close()
    def has_data(self):
        c=self.conn(); n=c.execute('select count(*) n from records').fetchone()['n']; c.close(); return n>0
    def replace(self, records, exceptions, truth):
        c=self.conn(); c.execute('delete from records'); c.execute('delete from exceptions');
        for r in records: c.execute('insert into records values(?,?,?)',(r['transaction_id'],json.dumps(r),json.dumps(truth.get(r['transaction_id'],{}))))
        for x in exceptions: c.execute('insert into exceptions values(?,?)',(x['exception_id'],json.dumps(x)))
        c.execute('insert into audit(event,detail) values(?,?)',('CONTROLLER_RUN',f'{len(records)} records, {len(exceptions)} exceptions'))
        c.commit(); c.close()
    def records(self):
        c=self.conn(); out=[json.loads(r['data']) for r in c.execute('select data from records')]; c.close(); return out
    def ground_truth(self):
        c=self.conn(); out={r['id']:json.loads(r['truth']) for r in c.execute('select id,truth from records')}; c.close(); return out
    def exceptions(self):
        c=self.conn(); out=[json.loads(r['data']) for r in c.execute('select data from exceptions order by json_extract(data,\'$.risk_score\') desc')]; c.close(); return out
    def exception(self,eid):
        c=self.conn(); r=c.execute('select data from exceptions where id=?',(eid,)).fetchone(); c.close(); return json.loads(r['data']) if r else None
    def audit(self):
        c=self.conn(); out=[dict(r) for r in c.execute('select * from audit order by id desc limit 100')]; c.close(); return out
    def policies(self): return [{'name':'Low-risk auto recommendation','rule':'risk_score < 31 and discrepancy < ₹100','action':'RECOMMEND_RESOLVE'}, {'name':'High-value review','rule':'discrepancy >= ₹10,000','action':'HUMAN_REVIEW'}, {'name':'Critical escalation','rule':'risk_score >= 81','action':'ESCALATE'}, {'name':'Duplicate protection','rule':'duplicate exception','action':'HUMAN_REVIEW'}]
    def review(self,eid,decision,note):
        c=self.conn(); c.execute('insert into reviews(exception_id,decision,note) values(?,?,?)',(eid,decision,note)); x=self.exception(eid); x['review_status']=decision; x['review_note']=note; c.execute('update exceptions set data=? where id=?',(json.dumps(x),eid)); c.execute('insert into audit(event,detail) values(?,?)',('HUMAN_DECISION',f'{eid}: {decision}')); c.commit(); c.close(); return x
store=Store()
