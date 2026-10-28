from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import engine, get_db

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Controle Financeiro API")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Controle Financeiro!"}

# --- Usuários ---
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return crud.create_user(db=db, user=user)

# --- Categorias ---
@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)

# --- Contas ---
@app.get("/accounts/{user_id}", response_model=List[schemas.Account])
def read_accounts(user_id: int, db: Session = Depends(get_db)):
    return crud.get_accounts(db, user_id=user_id)

@app.post("/accounts/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    return crud.create_account(db=db, account=account)

# --- Transações ---
@app.get("/transactions/{user_id}", response_model=List[schemas.Transaction])
def read_transactions(user_id: int, db: Session = Depends(get_db)):
    return crud.get_transactions(db, user_id=user_id)

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction)
