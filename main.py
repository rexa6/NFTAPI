from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend import database, models, crud
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Разрешаем запросы с фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можешь заменить на ["https://test24141.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def save_user(user: dict, db: Session = Depends(get_db)):
    u = crud.create_or_update_user(
        db,
        telegram_id=user["telegram_id"],
        username=user["username"],
        photo=user["photo"]
    )
    return {"status": "ok", "telegram_id": u.telegram_id}

# Получить инфу о юзере
@app.get("/users/{telegram_id}")
def get_user(telegram_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, telegram_id)
    if not user:
        return {"error": "User not found"}
    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "photo": user.photo,
        "balance": user.balance,
        "total_gifts": user.total_gifts,
        "gifts": [
            {"id": g.id, "image": g.image, "price": g.price}
            for g in user.gifts
        ]
    }

# Добавить новый подарок
@app.post("/users/{telegram_id}/add_gift")
def add_gift(telegram_id: int, gift: dict, db: Session = Depends(get_db)):
    g = crud.add_gift(db, telegram_id, gift["image"], gift["price"])
    if not g:
        return {"error": "User not found"}
    return {"status": "gift added", "gift_id": g.id}
