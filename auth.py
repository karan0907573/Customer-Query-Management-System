import hashlib
from db import get_user_by_username,create_user

def hashPassword(pswd):
    return hashlib.sha256(pswd.encode()).hexdigest()

def register_user(username, password, role='client'):
    existing = get_user_by_username(username)
    if existing:
        raise ValueError("username exists")
    hashed_password = hashPassword(password)
    return create_user(username, hashed_password, role)

def verify_password(password: str, password_hash: str) -> bool:
    return hashPassword(password) == password_hash

# def verify_password(username: str,password:str) -> bool:
#     user=get_user_by_username(username)
#     if(user):
#      return hashPassword(password) == user['hashed_password']
#     else:
#        return False