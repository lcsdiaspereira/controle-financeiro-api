from backend.database import SessionLocal
from backend.models import User
from backend import auth

def reset_password(email, new_password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email.strip().lower()).first()
        if user:
            hashed = auth.get_password_hash(new_password)
            user.hashed_password = hashed
            db.commit()
            print(f"Senha do usuário {email} resetada com sucesso para: {new_password}")
        else:
            print(f"Usuário com e-mail {email} não encontrado.")
    except Exception as e:
        print(f"Erro ao resetar senha: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Substitua pelo e-mail do usuário
    TARGET_EMAIL = "lcs.diaspereira@outlook.com"
    NEW_PASSWORD = "123456"
    reset_password(TARGET_EMAIL, NEW_PASSWORD)
