from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas, crud, auth
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Controle Financeiro Familiar API")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Servidor está online e respondendo!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = payload.get("sub")
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )
    return user

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"DEBUG: Login attempt for email: {form_data.username}")
    try:
        user = crud.get_user_by_email(db, email=form_data.username)
        if not user:
            print(f"DEBUG: User not found: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos"
            )

        if not auth.verify_password(form_data.password, user.hashed_password):
            print(f"DEBUG: Password mismatch for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos"
            )

        print(f"DEBUG: Login successful for: {form_data.username}")
        access_token = auth.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Unexpected error during login: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(f"DEBUG: Create user attempt: {user.email}")
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            print(f"DEBUG: User already exists: {user.email}")
            raise HTTPException(status_code=400, detail="Email já cadastrado")

        new_user = crud.create_user(db=db, user=user)
        print(f"DEBUG: User created successfully! ID: {new_user.id}")
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Unexpected error during signup: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# --- Membros da Família ---
@app.get("/members/", response_model=List[schemas.Member])
def read_members(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    household_id = current_user.member.household_id
    return crud.get_members_by_household(db, household_id=household_id)

@app.post("/members/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Membros são criados dentro da família do usuário logado
    household_id = current_user.member.household_id
    return crud.create_member(db=db, name=member.name, household_id=household_id, is_user=member.is_user)

# --- Contas ---
@app.get("/accounts/", response_model=List[schemas.Account])
def read_accounts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Retorna apenas as contas do membro logado
    return crud.get_accounts(db, member_id=current_user.member.id)

@app.post("/accounts/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    account.member_id = current_user.member.id
    account.household_id = current_user.member.household_id
    return crud.create_account(db=db, account=account)

@app.get("/accounts/{account_id}/balance", response_model=schemas.Balance)
def read_account_balance(account_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Verifica se a conta pertence à família do usuário
    account = db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.household_id == current_user.member.household_id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada ou acesso negado")

    balance_value = crud.get_account_balance(db, account_id=account_id)
    return schemas.Balance(account_id=account_id, balance=balance_value)

# --- Resumo e Gastos ---
@app.get("/summary/{year}/{month}", response_model=schemas.MonthlySummary)
def read_monthly_summary(year: int, month: int, view: str = "individual", db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    household_id = current_user.member.household_id
    member_id = current_user.member.id if view == "individual" else None

    summary_data = crud.get_monthly_summary(db, year=year, month=month, household_id=household_id, member_id=member_id)

    return {
        **summary_data,
        "view_type": view,
        "member_name": current_user.member.name if view == "individual" else "Família"
    }

@app.get("/expenses/{year}/{month}", response_model=List[schemas.CategoryExpense])
def read_expenses_by_category(year: int, month: int, view: str = "individual", db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    household_id = current_user.member.household_id
    member_id = current_user.member.id if view == "individual" else None

    return crud.get_expenses_by_category(db, year=year, month=month, household_id=household_id, member_id=member_id)

# --- Transações ---
@app.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(db: Session = Depends(get_db), view: str = "individual", current_user: models.User = Depends(get_current_user)):
    household_id = current_user.member.household_id
    member_id = current_user.member.id if view == "individual" else None
    return crud.get_transactions(db, household_id=household_id, member_id=member_id)

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Vincula a transação ao membro e à família
    transaction.member_id = transaction.member_id or current_user.member.id
    transaction.household_id = current_user.member.household_id
    return crud.create_transaction(db=db, transaction=transaction)
