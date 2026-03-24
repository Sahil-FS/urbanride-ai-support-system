import re
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Mock Intent Detection API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class DetectRequest(BaseModel):
    text: str

class DetectResponse(BaseModel):
    intent: str
    confidence: float

INTENT_RULES = [
    # ✅ EMERGENCY MUST BE FIRST — before safety_issue
    (r"sos|emergency.*help|help.*emergency|life.*danger|emergency.*danger|danger.*now|sos.*now|sos.*emergency|emergency.*sos", "emergency_sos", 0.99),

    # Greetings / General
    (r"hello|hi\b|hey\b|good morning|good evening|greet", "greeting", 0.92),
    (r"bye|goodbye|see you|take care", "goodbye", 0.90),
    (r"thank|thanks|appreciate|helpful", "thank_you", 0.91),
    (r"^help$|^assist$|what can you|how can you help", "help_request", 0.75),

    # ✅ Support contact — must be before fallback
    (r"talk.*support|call.*support|contact.*support|speak.*agent|human.*agent|live.*agent|agent.*human|contact.*agent", "contact_support", 0.95),

    # Ride tracking
    (r"where.*(driver|cab|car|ride)|track|locate|eta|arriving|how long", "track_ride", 0.91),
    (r"not.*(arriv|come|here|show)|waiting|driver.*(not|where)", "driver_not_arrived", 0.89),
    (r"driver.*(late|delay|slow|taking long)", "driver_late", 0.88),
    (r"cannot.*contact|not.*picking|not.*answering|unreachable", "cannot_contact_driver", 0.87),
    (r"wrong.*pickup|pickup.*wrong|different.*location", "wrong_pickup_location", 0.88),
    (r"wrong.*drop|drop.*wrong|change.*destination|new.*drop", "wrong_drop_location", 0.87),
    (r"started.*without|ride.*started.*not|moving.*without", "ride_started_without_user", 0.95),
    (r"not.*started|ride.*not.*begin|trip.*not.*start", "ride_not_started", 0.87),

    # Cancellation
    (r"cancel.*free|free.*cancel|no.*fee.*cancel|cancel.*no.*charge", "cancel_ride_free", 0.94),
    (r"driver.*cancel|cancelled.*driver|driver.*cancelled", "cancel_by_driver", 0.90),
    (r"cancellation.*fee|fee.*cancel|charged.*cancel", "cancellation_fee_issue", 0.89),
    (r"cancel|cancell|call off|abort|don.t want", "cancel_ride", 0.93),

    # Payment
    (r"payment.*fail|fail.*payment|transaction.*fail|declined", "payment_failed", 0.91),
    (r"double.*pay|charged.*twice|two.*charge|duplicate.*charge", "double_payment", 0.93),
    (r"overcharg|wrong.*fare|extra.*charge|too much.*fare|fare.*wrong", "wrong_fare_charged", 0.91),
    (r"change.*payment|add.*card|new.*card|update.*payment|add.*upi", "payment_method_change", 0.87),
    (r"payment.*issue|issue.*payment|pay.*problem|problem.*pay", "payment_issue", 0.92),

    # Dispute
    (r"dispute.*fare|dispute.*charge|dispute.*route|dispute.*payment", "dispute_charge", 0.91),

    # Refund
    (r"refund.*status|status.*refund|when.*refund|check.*refund", "refund_status", 0.90),
    (r"refund.*not.*received|not.*got.*refund|refund.*pending", "refund_not_received", 0.91),
    (r"escalate.*refund|urgent.*refund", "escalate_refund", 0.90),
    (r"refund|money back|return.*money|reimburse|new.*refund|request.*refund", "refund_request", 0.93),

    # Billing
    (r"invoice|receipt|bill|billing.*document", "invoice_request", 0.88),
    (r"fare.*breakup|breakup.*fare|fare.*detail|how.*fare.*calculated", "fare_breakup", 0.87),

    # ✅ Safety — AFTER emergency_sos
    (r"rude|misbehav|misconduct|behav.*bad|bad.*behav|inappropriate", "driver_misbehavior", 0.91),
    (r"rash|fast.*driv|driv.*fast|speed|over.*speed|rashly", "rash_driving", 0.90),
    (r"accident|crash|collision|hit", "accident_report", 0.95),
    (r"unsafe|danger|threat|harass|scared|safety|safety concern|report.*driver|driver.*report", "safety_issue", 0.95),

    # Lost item
    (r"lost|forgot|left.*(bag|phone|wallet|item)|missing.*(item|thing)", "lost_item", 0.92),

    # Account
    (r"login|sign.?in|password|otp|access|locked", "login_problem", 0.89),
    (r"update.*profile|change.*name|change.*number|edit.*profile", "update_profile", 0.87),
    (r"account.*issue|issue.*account|profile.*problem", "account_issue", 0.89),

    # Coupons
    (r"offer.*not.*apply|coupon.*not.*work|promo.*fail", "offer_not_applied", 0.88),
    (r"retry.*coupon|coupon.*again|promo.*again", "apply_coupon", 0.88),
    (r"promo|coupon|discount|offer.*code|code.*offer|apply.*code", "apply_coupon", 0.88),

    # Route
    (r"long.*route|longer.*route|extra.*km|unnecessary.*route", "long_route_taken", 0.89),
    (r"wrong.*route|route.*wrong|route.*issue", "route_issue", 0.88),

    # Driver issue generic — catches "driver issue" button
    (r"driver.*issue|issue.*driver|problem.*driver|driver.*problem", "safety_issue", 0.88),
]

def classify(text: str) -> tuple[str, float]:
    text_lower = text.lower().strip()
    for pattern, intent, base_conf in INTENT_RULES:
        if re.search(pattern, text_lower):
            noise = random.uniform(-0.02, 0.02)
            confidence = round(min(1.0, max(0.6, base_conf + noise)), 4)
            return intent, confidence
    return "unknown_intent", round(random.uniform(0.20, 0.40), 4)

@app.post("/detect", response_model=DetectResponse)
def detect_intent(req: DetectRequest):
    intent, confidence = classify(req.text)
    return DetectResponse(intent=intent, confidence=confidence)

@app.get("/health")
def health():
    return {"status": "ok", "service": "mock-intent-api", "port": 8001}

@app.get("/intents")
def list_intents():
    return {"intents": [r[1] for r in INTENT_RULES] + ["unknown_intent"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mock_intent_api:app", host="0.0.0.0", port=8001, reload=True)