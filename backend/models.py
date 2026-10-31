from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Household(Base):
    __tablename__ = "households"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), default="Minha Família")

    members = relationship("Member", back_populates="household")
    accounts = relationship("Account", back_populates="household")
    transactions = relationship("Transaction", back_populates="household")

class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    household_id = Column(Integer, ForeignKey("households.id"))
    is_user = Column(Boolean, default=True) # True se tiver login, False se for dependente

    household = relationship("Household", back_populates="members")
    user = relationship("User", back_populates="member", uselist=False)
    accounts = relationship("Account", back_populates="member")
    transactions = relationship("Transaction", back_populates="member")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))

    member = relationship("Member", back_populates="user")

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    type = Column(String(50))
    member_id = Column(Integer, ForeignKey("members.id"))
    household_id = Column(Integer, ForeignKey("households.id"))

    member = relationship("Member", back_populates="accounts")
    household = relationship("Household", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    type = Column(String(50)) # "Entrada" ou "Saida"

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255))
    amount = Column(Float)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    member_id = Column(Integer, ForeignKey("members.id"))
    household_id = Column(Integer, ForeignKey("households.id"))

    member = relationship("Member", back_populates="transactions")
    household = relationship("Household", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category")
