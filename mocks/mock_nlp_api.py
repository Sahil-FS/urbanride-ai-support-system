from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Mock NLP API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class TranslateRequest(BaseModel):
    text: str

class TranslateResponse(BaseModel):
    detected_language: str
    translated_text: str

TRANSLATION_MAP = {
    "मेरी राइड रद्द करें": ("hi", "Cancel my ride"),
    "मेरा ड्राइवर कहाँ है": ("hi", "Where is my driver"),
    "भुगतान की समस्या है": ("hi", "I have a payment issue"),
    "पैसे वापस चाहिए": ("hi", "I want a refund"),
    "ड्राइवर नहीं आया": ("hi", "Driver has not arrived"),
    "मेरा सामान छूट गया": ("hi", "I lost my item in the cab"),
    "किराया ज्यादा लगा": ("hi", "I was overcharged for the fare"),
    "ऐप काम नहीं कर रहा": ("hi", "The app is not working"),
    "मुझे मदद चाहिए": ("hi", "I need help"),
    "माझी राईड रद्द करा": ("mr", "Cancel my ride"),
    "माझा ड्रायव्हर कुठे आहे": ("mr", "Where is my driver"),
    "पेमेंट समस्या आहे": ("mr", "I have a payment issue"),
    "मला मदत हवी": ("mr", "I need help"),
    "meri ride cancel karo": ("hi", "Cancel my ride"),
    "driver kahan hai": ("hi", "Where is my driver"),
    "payment issue hai": ("hi", "I have a payment issue"),
    "refund chahiye": ("hi", "I want a refund"),
    "driver nahi aaya": ("hi", "Driver has not arrived"),
    "app kaam nahi kar raha": ("hi", "The app is not working"),
    "mujhe madad chahiye": ("hi", "I need help"),
}

def detect_and_translate(text: str) -> tuple[str, str]:
    stripped = text.strip()
    if stripped in TRANSLATION_MAP:
        return TRANSLATION_MAP[stripped]
    if stripped.lower() in TRANSLATION_MAP:
        return TRANSLATION_MAP[stripped.lower()]
    ascii_ratio = sum(1 for c in stripped if ord(c) < 128) / max(len(stripped), 1)
    if ascii_ratio > 0.85:
        return "en", stripped
    return "unknown", stripped

@app.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    lang, translated = detect_and_translate(req.text)
    return TranslateResponse(detected_language=lang, translated_text=translated)

@app.get("/health")
def health():
    return {"status": "ok", "service": "mock-nlp-api", "port": 8002}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mock_nlp_api:app", host="0.0.0.0", port=8002, reload=True)
