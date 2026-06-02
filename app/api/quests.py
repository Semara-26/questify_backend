from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.game_logic import calculate_quest_reward, process_level_up
from app.models.models import Quest, User
from app.schemas import QuestCreate, QuestResponse

router = APIRouter()


@router.get("/", response_model=List[QuestResponse])
def get_quests(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    quests = db.query(Quest).filter(Quest.user_id == current_user.id).all()
    return quests


@router.post("/", response_model=QuestResponse)
def create_quest(
    quest_in: QuestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_quest = Quest(
        title=quest_in.title,
        rank=quest_in.rank,
        user_id=current_user.id,
        status="active",
    )
    db.add(db_quest)
    db.commit()
    db.refresh(db_quest)
    return db_quest


@router.put("/{quest_id}/complete", response_model=QuestResponse)
def complete_quest(
    quest_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quest = (
        db.query(Quest)
        .filter(Quest.id == quest_id, Quest.user_id == current_user.id)
        .first()
    )
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    if quest.status == "completed":
        raise HTTPException(status_code=400, detail="Quest already completed")

    quest.status = "completed"

    try:
        earned_exp, earned_coins = calculate_quest_reward(quest.rank)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Update user stats
    current_user.coins += earned_coins
    new_level, new_exp = process_level_up(
        current_user.level, current_user.exp + earned_exp
    )
    current_user.level = new_level
    current_user.exp = new_exp

    db.commit()
    db.refresh(quest)
    return quest


@router.delete("/{quest_id}")
def delete_quest(
    quest_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quest = db.query(Quest).filter(Quest.id == quest_id).first()

    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    if quest.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Forbidden: You cannot delete someone else's quest"
        )

    db.delete(quest)
    db.commit()

    return {"detail": "Quest berhasil dihapus"}


@router.put("/{quest_id}", response_model=QuestResponse)
def update_quest(
    quest_id: UUID,
    quest_in: QuestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quest = db.query(Quest).filter(Quest.id == quest_id).first()

    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    if quest.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Forbidden: You cannot edit someone else's quest"
        )

    if quest.status == "completed":
        raise HTTPException(
            status_code=400, detail="Quest yang sudah selesai tidak dapat diedit"
        )

    # Lakukan Update Data
    quest.title = quest_in.title
    quest.rank = quest_in.rank

    db.commit()
    db.refresh(quest)
    return quest
