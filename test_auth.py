import sys
sys.path.append('.')
from backend.database import SessionLocal
from backend import crud, auth, schemas
from backend.models import User

def test():
    db = SessionLocal()
    email = "test_claude@example.com"
    password = "StrongPassword123!"
    name = "Claude Test"

    print(f"--- Testing User: {email} ---")

    # 1. Check if user exists
    user = crud.get_user_by_email(db, email)
    if user:
        print(f"User {email} already exists. Deleting for clean test...")
        db.delete(user)
        db.commit()

    # 2. Create User
    print("Creating user...")
    try:
        user_create = schemas.UserCreate(email=email, password=password, name=name)
        new_user = crud.create_user(db, user_create)
        print(f"User created successfully! ID: {new_user.id}")
    except Exception as e:
        print(f"Error creating user: {e}")
        return

    # 3. Try to create again
    print("Trying to create same user again...")
    user_exists = crud.get_user_by_email(db, email)
    if user_exists:
        print("Success: get_user_by_email found the user (would raise 'Email já cadastrado').")
    else:
        print("Failure: get_user_by_email did NOT find the user.")

    # 4. Try to login (verify password)
    print("Testing password verification...")
    if user_exists:
        is_valid = auth.verify_password(password, user_exists.hashed_password)
        print(f"Password verification result: {'SUCCESS' if is_valid else 'FAILURE'}")
        
        # Try wrong password
        is_valid_wrong = auth.verify_password("WrongPassword", user_exists.hashed_password)
        print(f"Wrong password verification result: {'SUCCESS' if is_valid_wrong else 'FAILURE'}")
    else:
        print("Cannot verify password, user not found.")

    db.close()

if __name__ == "__main__":
    test()
