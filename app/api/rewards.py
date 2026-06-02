from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.game_logic import process_shop_payment
from app.models.models import Reward, User
from app.schemas import RewardCreate, RewardResponse

router = APIRouter()


@router.get("/", response_model=List[RewardResponse])
def get_rewards(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    rewards = db.query(Reward).filter(Reward.is_active == True).all()
    return rewards


@router.post("/", response_model=RewardResponse)
def create_reward(
    reward_in: RewardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_reward = Reward(title=reward_in.title, cost=reward_in.cost, is_active=True)
    db.add(db_reward)
    db.commit()
    db.refresh(db_reward)
    return db_reward


@router.post("/redeem/{reward_id}")
def redeem_reward(
    reward_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")

    if not reward.is_active:
        raise HTTPException(status_code=400, detail="Reward is not active")

    try:
        remaining_coins = process_shop_payment(current_user.coins, reward.cost)
        current_user.coins = remaining_coins
        db.commit()
        return {
            "detail": "Reward redeemed successfully",
            "remaining_coins": remaining_coins,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
