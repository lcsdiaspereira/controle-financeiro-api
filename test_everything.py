import sys
import os
sys.path.append(os.getcwd())

from backend.database import SessionLocal
from backend import crud, auth, schemas, models

def run_full_test():
    db = SessionLocal()
    print("=== INICIANDO TESTE GERAL DE FLUXO ===")
    
    test_email = "final_test@example.com"
    test_password = "SecurePassword123!"
    test_name = "Usuario Teste"

    try:
        # 1. Limpeza
        print(f"\n[1/4] Limpando dados de teste ({test_email})...")
        user = crud.get_user_by_email(db, test_email)
        if user:
            # To delete a user, we might need to delete related data first
            # But for a simple test, let's just delete the user
            db.delete(user)
            db.commit()
            print("Usuário antigo removido.")
        else:
            print("Nenhum usuário antigo encontrado.")

        # 2. Teste de Cadastro
        print(f"\n[2/4] Testando Cadastro...")
        user_create = schemas.UserCreate(email=test_email, password=test_password, name=test_name)
        try:
            new_user = crud.create_user(db, user_create)
            print(f"SUCESSO: Usuário criado com ID {new_user.id}")
        except Exception as e:
            print(f"FALHA no Cadastro: {str(e)}")
            import traceback
            traceback.print_exc()
            return

        # 3. Teste de Busca/Existência
        print(f"\n[3/4] Testando Verificação de Existência...")
        found_user = crud.get_user_by_email(db, test_email)
        if found_user and found_user.id == new_user.id:
            print("SUCESSO: Usuário encontrado corretamente.")
        else:
            print("FALHA: Usuário não foi encontrado após a criação.")
            return

        # 4. Teste de Login (Senha)
        print(f"\n[4/4] Testando Verificação de Senha...")
        if auth.verify_password(test_password, found_user.hashed_password):
            print("SUCESSO: Senha validada corretamente.")
        else:
            print("FALHA: Senha NÃO validou.")
            return

        print("\n==========================================")
        print("RESULTADO FINAL: FLUXO DE AUTH ESTÁ FUNCIONANDO!")
        print("==========================================")

    except Exception as e:
        print(f"\nERRO CRÍTICO DURANTE TESTE: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    run_full_test()
