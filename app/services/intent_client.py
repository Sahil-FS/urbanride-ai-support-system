import logging
import httpx
from app.core.config import settings
from app.models.schemas import IntentResult

logger = logging.getLogger(__name__)

async def detect_intent(text: str) -> IntentResult:
    try:
        async with httpx.AsyncClient(timeout=settings.EXTERNAL_API_TIMEOUT) as client:
            resp = await client.post(settings.INTENT_API_URL, json={"text": text})
            resp.raise_for_status()
            data = resp.json()
            return IntentResult(
                intent=data.get("intent", "unknown_intent"),
                confidence=float(data.get("confidence", 0.0)),
            )
    except Exception as exc:
        logger.error("Intent API error: %s", exc)
        return IntentResult(intent="unknown_intent", confidence=0.0)
