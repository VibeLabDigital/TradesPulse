#!/usr/bin/env python
"""
TradesPulse FastAPI Server
--------------------------
This is the "doorbell" that lets Replit, Jobber webhooks,
Twilio, and other services trigger your crewAI crews.

HOW TO RUN:
    pip install fastapi uvicorn
    uvicorn api:app --host 0.0.0.0 --port 8000

REPLIT:
    Set CREWAI_SERVER_URL to your Replit public URL
    e.g. https://tradespulse.yourname.repl.co
"""

import os
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from tradespulse___home_service_automation.crew import TradespulseHomeServiceAutomationCrew

app = FastAPI(title="TradesPulse Agent API", version="1.0.0")

# Allow Replit and your landing page to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────

class TriggerRequest(BaseModel):
    trigger: str          # Which workflow to run (see TRIGGERS below)
    business_name: str    # The client's business name
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    job_id: Optional[str] = None
    quote_id: Optional[str] = None
    extra: Optional[dict] = None  # Any additional context

# ─────────────────────────────────────────
# TRIGGER → INPUTS MAPPING
# Maps each trigger name to the inputs your crew needs
# ─────────────────────────────────────────

TRIGGERS = {
    # Inbound Lead Capture Specialist
    "missed_call":        ["business_name", "customer_name", "customer_phone"],
    "web_form_lead":      ["business_name", "customer_name", "customer_email", "customer_phone"],

    # Quote Follow Up Specialist
    "quote_sent":         ["business_name", "customer_name", "quote_id"],
    "quote_follow_up":    ["business_name", "customer_name", "quote_id"],

    # Post Job Customer Experience Manager
    "job_complete":       ["business_name", "customer_name", "job_id"],
    "review_request":     ["business_name", "customer_name", "customer_phone"],

    # Seasonal Campaign Manager
    "seasonal_campaign":  ["business_name"],
    "lapsed_customer":    ["business_name", "customer_name"],

    # Operations Manager
    "workflow_check":     ["business_name"],
    "weekly_report":      ["business_name"],
}

# ─────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────

@app.get("/")
def health_check():
    return {
        "status": "TradesPulse API is running",
        "timestamp": datetime.utcnow().isoformat(),
        "available_triggers": list(TRIGGERS.keys())
    }

# ─────────────────────────────────────────
# MAIN TRIGGER ENDPOINT
# This is what Replit's Integration Hub calls
# ─────────────────────────────────────────

@app.post("/trigger")
def trigger_crew(request: TriggerRequest):
    """
    Trigger a TradesPulse crew workflow.
    
    Example body:
    {
        "trigger": "missed_call",
        "business_name": "Acme Plumbing",
        "customer_name": "John Smith",
        "customer_phone": "+15551234567"
    }
    """
    if request.trigger not in TRIGGERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown trigger '{request.trigger}'. Valid triggers: {list(TRIGGERS.keys())}"
        )

    # Build inputs from the request
    inputs = {
        "trigger": request.trigger,
        "business_name": request.business_name,
        "customer_name": request.customer_name or "Valued Customer",
        "customer_phone": request.customer_phone or "",
        "customer_email": request.customer_email or "",
        "job_id": request.job_id or "",
        "quote_id": request.quote_id or "",
        "current_date": datetime.utcnow().strftime("%Y-%m-%d"),
        **(request.extra or {})
    }

    try:
        result = TradespulseHomeServiceAutomationCrew().crew().kickoff(inputs=inputs)
        return {
            "status": "success",
            "trigger": request.trigger,
            "business": request.business_name,
            "result": str(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crew error: {str(e)}")


# ─────────────────────────────────────────
# TWILIO WEBHOOK ENDPOINT
# Twilio calls this when a call is missed
# ─────────────────────────────────────────

@app.post("/webhooks/twilio/missed-call")
def twilio_missed_call(
    From: str = "",       # Twilio sends caller number as "From"
    To: str = "",         # Your Twilio number
    CallStatus: str = ""
):
    """
    Twilio posts here automatically when a call is missed.
    Wire this URL in your Twilio console under
    'A call comes in' → webhook → this URL + /webhooks/twilio/missed-call
    """
    inputs = {
        "trigger": "missed_call",
        "business_name": os.getenv("BUSINESS_NAME", "TradesPulse Client"),
        "customer_name": "Unknown Caller",
        "customer_phone": From,
        "current_date": datetime.utcnow().strftime("%Y-%m-%d"),
    }

    try:
        result = TradespulseHomeServiceAutomationCrew().crew().kickoff(inputs=inputs)
        # Twilio expects TwiML back - return empty response to avoid error
        return {"status": "handled", "caller": From}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# JOBBER WEBHOOK ENDPOINT
# Jobber calls this when jobs/quotes change
# ─────────────────────────────────────────

@app.post("/webhooks/jobber")
def jobber_webhook(payload: dict):
    """
    Jobber posts here on events like:
    - quote.approved
    - job.completed
    - request.created
    Wire this URL in Jobber Settings → Connected Apps → Webhooks
    """
    event = payload.get("webHookEvent", "")
    data = payload.get("data", {})

    # Map Jobber events to your triggers
    trigger_map = {
        "QUOTE_APPROVAL_STATUS_CHANGED": "quote_sent",
        "JOB_COMPLETION_STATUS_CHANGED": "job_complete",
        "REQUEST_CREATED": "web_form_lead",
    }

    trigger = trigger_map.get(event)
    if not trigger:
        return {"status": "ignored", "event": event}

    inputs = {
        "trigger": trigger,
        "business_name": os.getenv("BUSINESS_NAME", "TradesPulse Client"),
        "customer_name": data.get("client", {}).get("name", "Customer"),
        "customer_phone": data.get("client", {}).get("phone", ""),
        "customer_email": data.get("client", {}).get("email", ""),
        "job_id": str(data.get("jobId", "")),
        "quote_id": str(data.get("quoteId", "")),
        "current_date": datetime.utcnow().strftime("%Y-%m-%d"),
    }

    try:
        result = TradespulseHomeServiceAutomationCrew().crew().kickoff(inputs=inputs)
        return {"status": "success", "trigger": trigger}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# WEEKLY REPORT ENDPOINT
# Call this via a cron job every Monday
# ─────────────────────────────────────────

@app.post("/schedule/weekly-report")
def weekly_report():
    """
    Trigger the weekly business intelligence report.
    Set up a cron job or Replit scheduled task to hit this every Monday at 9am.
    """
    inputs = {
        "trigger": "weekly_report",
        "business_name": os.getenv("BUSINESS_NAME", "TradesPulse Client"),
        "current_date": datetime.utcnow().strftime("%Y-%m-%d"),
    }
    try:
        result = TradespulseHomeServiceAutomationCrew().crew().kickoff(inputs=inputs)
        return {"status": "success", "report": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
