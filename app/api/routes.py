from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.ledger.service import LedgerService
from app.pricing.engine import PricingEngine

router = APIRouter()
ledger = LedgerService()
pricing = PricingEngine()

class EarnIn(BaseModel):
    user_id: str
    base_points: int = Field(ge=1)
    reason: str = "purchase"

class QuoteIn(BaseModel):
    user_id: str
    reward_id: str
    list_price_points: int = Field(ge=1)

class ReserveIn(BaseModel):
    user_id: str
    points: int = Field(ge=1)

@router.post("/earn")
def earn(payload: EarnIn):
    txn = ledger.earn(user_id=payload.user_id, base_points=payload.base_points, reason=payload.reason)
    return {"txn_id": txn}

@router.post("/quote")
def quote(payload: QuoteIn):
    price = pricing.quote_burn_price(
        user_id=payload.user_id,
        reward_id=payload.reward_id,
        list_price_points=payload.list_price_points,
    )
    return {"reward_id": payload.reward_id, "price_points": price}

@router.post("/reserve")
def reserve(payload: ReserveIn):
    ok, hold_id = ledger.reserve(user_id=payload.user_id, points=payload.points)
    if not ok:
        raise HTTPException(status_code=400, detail="insufficient_points")
    return {"hold_id": hold_id}

@router.get("/balance/{user_id}")
def balance(user_id: str):
    return ledger.balance(user_id=user_id)

@router.get("/liability")
def liability():
    return ledger.liability()
