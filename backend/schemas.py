from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CategoryBase(BaseModel):
    name: str
    type: str # "Entrada" ou "Saida"

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class AccountBase(BaseModel):
    name: str
    type: str

class AccountCreate(AccountBase):
    user_id: int

class Account(AccountBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    description: str
    amount: float
    date: datetime
    category_id: int
    account_id: int
    user_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True
