from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime, timezone

from backend.schemas.models import RawReport
from backend.security.auth import get_current_reviewer, get_current_admin
from backend.security.rate_limiter import check_rate_limit
from backend.security.input_sanitization import sanitize_report_text
from backend.graph.build_graph import build_coordinator_graph

router = APIRouter()
graph = build_coordinator_graph()

class ReportSubmission(BaseModel):
    source_channel: str
    raw_text: str
    reporter_contact: Optional[str] = None

@router.post("/reports", dependencies=[Depends(check_rate_limit)])
async def submit_report(submission: ReportSubmission):
    sanitized = sanitize_report_text(submission.raw_text)
    if not sanitized:
        raise HTTPException(status_code=400, detail="Invalid report text")
        
    report = RawReport(
        report_id=f"rpt-{uuid.uuid4().hex[:8]}",
        source_channel=submission.source_channel,
        raw_text=sanitized,
        submitted_at=datetime.now(timezone.utc),
        reporter_contact=submission.reporter_contact
    )
    
    # In a real app, we would save to DB here and kick off the graph asynchronously.
    # For the demo, we will stream the graph synchronously so we can see the result immediately.
    config = {"configurable": {"thread_id": report.report_id}}
    state = {"raw_report": report}
    
    # Run the graph until completion or interrupt
    for event in graph.stream(state, config, stream_mode="values"):
        pass
        
    # Get the latest state
    final_state = graph.get_state(config)
    
    if final_state.next and "human_review" in final_state.next:
        return {"status": "pending_review", "report_id": report.report_id}
        
    return {"status": "processed", "report_id": report.report_id}

@router.get("/reports/{report_id}")
async def get_report_status(report_id: str, current_user: dict = Depends(get_current_reviewer)):
    config = {"configurable": {"thread_id": report_id}}
    state = graph.get_state(config)
    
    if not state or not state.values:
        raise HTTPException(status_code=404, detail="Report not found")
        
    return {
        "report_id": report_id,
        "extracted_need": state.values.get("extracted_need"),
        "verified_need": state.values.get("verified_need"),
        "pending_review": "human_review" in state.next
    }

@router.get("/review/queue")
async def get_review_queue(current_user: dict = Depends(get_current_reviewer)):
    # In a real app, this would query the DB for needs where requires_human_review = True
    return {"queue": []}

@router.post("/review/{need_id}")
async def review_need(need_id: str, action: str, current_user: dict = Depends(get_current_reviewer)):
    # Mocking graph resumption. Assuming thread_id matches need_id (or lookup).
    # action should be 'approve' or 'reject'
    return {"status": "resumed"}

@router.get("/resources")
async def get_resources(current_user: dict = Depends(get_current_admin)):
    return {"resources": []}

@router.post("/resources")
async def add_resource(current_user: dict = Depends(get_current_admin)):
    return {"status": "added"}

@router.get("/plans/{plan_id}")
async def get_plan(plan_id: str, current_user: dict = Depends(get_current_reviewer)):
    return {"plan": "details"}

@router.post("/plans/{plan_id}/override")
async def override_plan(plan_id: str, current_user: dict = Depends(get_current_admin)):
    return {"status": "overridden"}
