from backend.database import SessionLocal
from backend import crud, schemas
import sys

def test_create_user():
    db = SessionLocal()
    try:
        user_data = schemas.UserCreate(
            email="lcs.diaspereira@outlook.com",
            password="123",
            name="Lucas Dias Pereira"
        )
        print(f"Tentando criar usuário: {user_data.email}...")
        user = crud.create_user(db=db, user=user_data)
        print(f"Sucesso! Usuário criado com ID: {user.id}")
    except Exception as e:
        print(f"ERRO REAL: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_create_user()
