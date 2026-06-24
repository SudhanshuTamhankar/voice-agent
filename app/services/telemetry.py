import json
import time
import os
from datetime import datetime
from typing import Dict, Any

class TelemetryService:
    def __init__(self, analytics_file="analytics.jsonl", audit_file="audit.jsonl"):
        self.analytics_file = analytics_file
        self.audit_file = audit_file
        
    def _write_jsonl(self, file_path: str, data: Dict[str, Any]):
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(data) + "\n")
        except Exception as e:
            print(f"[Telemetry Error] Could not write to {file_path}: {e}")

    def track_event(self, event_name: str, session_id: str, payload: Dict[str, Any] = None):
        """
        Logs a product usage event to analytics.jsonl
        """
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": event_name,
            "session_id": session_id,
            "payload": payload or {}
        }
        self._write_jsonl(self.analytics_file, event)

    def log_audit_trace(self, session_id: str, turn_id: str, user_query: str, intent: str, 
                        extracted_profile: dict, response_plan: dict, final_answer: str, 
                        guardrail_passed: bool):
        """
        Logs a full deterministic trace of an interaction to audit.jsonl for reproducibility.
        """
        trace = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "session_id": session_id,
            "turn_id": turn_id,
            "user_query": user_query,
            "intent": intent,
            "profile_snapshot": extracted_profile,
            "response_plan": response_plan,
            "final_answer": final_answer,
            "guardrail_passed": guardrail_passed
        }
        self._write_jsonl(self.audit_file, trace)
