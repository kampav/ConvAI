from datetime import datetime, timezone
import json
from pathlib import Path
from threading import Lock
class AuditStore:
    def __init__(self,path:str="./data/audit.jsonl"): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True); self._lock=Lock()
    def record(self,event_type:str,trace_id:str,data:dict):
        event={"timestamp":datetime.now(timezone.utc).isoformat(),"event_type":event_type,"trace_id":trace_id,"data":data}
        with self._lock,self.path.open("a",encoding="utf-8") as f: f.write(json.dumps(event,default=str)+"\n")
    def find_by_conversation(self,conversation_id:str):
        if not self.path.exists(): return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if conversation_id in line]
