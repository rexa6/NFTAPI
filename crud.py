from sqlalchemy.orm import Session
from . import models

def create_or_update_user(db: Session, telegram_id: int, username: str, photo: str):
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if not user:
        user = models.User(
            telegram_id=telegram_id,
            username=username,
            photo=photo,
            balance=1000
        )
        db.add(user)
    else:
        user.username = username
        user.photo = photo
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, telegram_id: int):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()

def add_gift(db: Session, telegram_id: int, image: str, price: int):
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if not user:
        return None

    gift = models.Gift(image=image, price=price, owner=user)
    db.add(gift)
    db.commit()
    db.refresh(gift)
    return gift
