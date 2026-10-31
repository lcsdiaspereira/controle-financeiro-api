from backend.database import SessionLocal
from backend.models import User

def check_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"Total de usuários no banco: {len(users)}")
        for user in users:
            print(f"ID: {user.id} | Email: {user.email} | Nome: {user.member.name}")
    except Exception as e:
        print(f"Erro ao consultar banco: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
