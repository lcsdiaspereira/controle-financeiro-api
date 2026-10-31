from backend.database import engine
from backend.models import Base

def reset_database():
    try:
        print("Limpando banco de dados completamente...")
        # Remove todas as tabelas do banco de dados
        Base.metadata.drop_all(bind=engine)
        print("Tabelas removidas com sucesso!")

        # Recria todas as tabelas com a nova estrutura
        Base.metadata.create_all(bind=engine)
        print("Tabelas recriadas com a nova estrutura de Família!")
    except Exception as e:
        print(f"Erro ao resetar o banco: {e}")

if __name__ == "__main__":
    reset_database()
