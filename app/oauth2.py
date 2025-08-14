from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models, utils
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    print("Waktu expire UTC:", expire)
    print("Waktu expire WIB:", expire.astimezone(timezone(timedelta(hours=7))))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            return None
        token_data = schemas.TokenData(id=id)
    except jwt.ExpiredSignatureError:
        return None
    except JWTError:
        return None
    return token_data
    
def get_current_user(request: Request, db: Session = Depends(database.get_db)):
    token = request.cookies.get("access_token")
    if not token:
        print("no login")
        return "no_login"
    token_data = verify_access_token(token)
    if not token_data:  
        print("expired")
        return "expired"
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    print("ada token")
    return user