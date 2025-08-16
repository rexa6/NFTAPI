from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String)
    photo = Column(String)
    balance = Column(Integer, default=1000)

    gifts = relationship("Gift", back_populates="owner", cascade="all, delete")

    @property
    def total_gifts(self):
        return len(self.gifts)


class Gift(Base):
    __tablename__ = "gifts"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    price = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="gifts")
