from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# --- Modelos de Família ---
class HouseholdBase(BaseModel):
    name: str

class HouseholdCreate(HouseholdBase):
    pass

class Household(HouseholdBase):
    id: int
    class Config:
        from_attributes = True

# --- Modelos de Membro ---
class MemberBase(BaseModel):
    name: str
    household_id: int

class MemberCreate(MemberBase):
    is_user: bool = True

class Member(MemberBase):
    id: int
    is_user: bool
    class Config:
        from_attributes = True

# --- Modelos de Usuário ---
class UserBase(BaseModel):
    email: str
    member_id: Optional[int] = None

class UserCreate(UserBase):
    password: str
    name: str # Nome será usado para criar o Member
    account_name: Optional[str] = "Conta Principal"
    account_type: Optional[str] = "Corrente"

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

# --- Modelos de Conta ---
class AccountBase(BaseModel):
    name: str
    type: str

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    member_id: int
    household_id: int
    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str
    type: str

class Balance(BaseModel):
    account_id: int
    balance: float

# --- Modelos de Resumo ---
class MonthlySummary(BaseModel):
    year: int
    month: int
    total_income: float
    total_expense: float
    net_balance: float
    view_type: str # "individual" ou "household"
    member_name: Optional[str] = None

class CategoryExpense(BaseModel):
    category: str
    total: float

# --- Modelos de Transação ---
class TransactionBase(BaseModel):
    description: str
    amount: float
    date: datetime
    category_id: int
    account_id: int

class TransactionCreate(TransactionBase):
    member_id: Optional[int] = None
    household_id: Optional[int] = None

class Transaction(TransactionBase):
    id: int
    member_id: int
    household_id: int
    class Config:
        from_attributes = True
