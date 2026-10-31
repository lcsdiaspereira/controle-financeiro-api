from sqlalchemy.orm import Session
from sqlalchemy import func, case, extract
from . import models, schemas, auth

# --- Categorias ---
def get_categories(db: Session):
    return db.query(models.Category).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# --- Família e Membros ---
def create_household(db: Session, name: str = "Minha Família"):
    household = models.Household(name=name)
    db.add(household)
    db.commit()
    db.refresh(household)
    return household

def create_member(db: Session, name: str, household_id: int, is_user: bool = True):
    member = models.Member(name=name, household_id=household_id, is_user=is_user)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def get_members_by_household(db: Session, household_id: int):
    return db.query(models.Member).filter(models.Member.household_id == household_id).all()

# --- Contas ---
def get_accounts(db: Session, member_id: int):
    return db.query(models.Account).filter(models.Account.member_id == member_id).all()

def get_household_accounts(db: Session, household_id: int):
    return db.query(models.Account).filter(models.Account.household_id == household_id).all()

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# --- Saldo ---
def get_account_balance(db: Session, account_id: int):
    balance = db.query(
        func.sum(
            case(
                (models.Category.type == "Entrada", models.Transaction.amount),
                else_=-models.Transaction.amount
            )
        )
    ).join(models.Category).filter(models.Transaction.account_id == account_id).scalar()
    return balance or 0.0

# --- Resumo ---
def get_monthly_summary(db: Session, year: int, month: int, household_id: int, member_id: int = None):
    # Se member_id for fornecido, filtra por membro. Caso contrário, soma a família toda.
    query = db.query(
        func.sum(case((models.Category.type == "Entrada", models.Transaction.amount), else_=0)).label("income"),
        func.sum(case((models.Category.type == "Saida", models.Transaction.amount), else_=0)).label("expense")
    ).join(models.Category).filter(
        models.Transaction.household_id == household_id,
        extract('year', models.Transaction.date) == year,
        extract('month', models.Transaction.date) == month
    )

    if member_id:
        query = query.filter(models.Transaction.member_id == member_id)

    result = query.first()
    total_income = result.income or 0.0
    total_expense = result.expense or 0.0

    return {
        "year": year,
        "month": month,
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    }

def get_expenses_by_category(db: Session, year: int, month: int, household_id: int, member_id: int = None):
    query = db.query(
        models.Category.name.label("category"),
        func.sum(models.Transaction.amount).label("total")
    ).join(models.Category).filter(
        models.Transaction.household_id == household_id,
        models.Category.type == "Saida",
        extract('year', models.Transaction.date) == year,
        extract('month', models.Transaction.date) == month
    ).group_by(models.Category.name)

    if member_id:
        query = query.filter(models.Transaction.member_id == member_id)

    results = query.all()
    return [{"category": r.category, "total": r.total} for r in results]

# --- Transações ---
def get_transactions(db: Session, household_id: int, member_id: int = None):
    query = db.query(models.Transaction).filter(models.Transaction.household_id == household_id)
    if member_id:
        query = query.filter(models.Transaction.member_id == member_id)
    return query.all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# --- Usuários ---
def get_user_by_email(db: Session, email: str):
    clean_email = email.strip().lower()
    return db.query(models.User).filter(models.User.email == clean_email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # 1. Cria a Família
    household = create_household(db, name="Minha Família")

    # 2. Cria o Membro vinculado à Família
    member = create_member(db, name=user.name, household_id=household.id, is_user=True)

    # 3. Cria o Usuário vinculado ao Membro
    db_user = models.User(
        member_id=member.id,
        email=user.email.strip().lower(),
        hashed_password=auth.get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 4. Cria a Primeira Conta automaticamente
    account_data = schemas.AccountCreate(
        name=user.account_name or "Conta Principal",
        type=user.account_type or "Corrente"
    )
    # Adicionando manualmente os IDs necessários que o create_account espera via main.py
    # mas como estamos no crud, vamos criar o objeto Account diretamente
    db_account = models.Account(
        name=account_data.name,
        type=account_data.type,
        member_id=member.id,
        household_id=household.id
    )
    db.add(db_account)
    db.commit()

    return db_user
