from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

class AuthService:
  
  def __init__(self):
    self.pwd_context = CryptContext(
      schemes=["bcrypt"],
      deprecated="auto",
      bcrypt__rounds=settings.bcrypt_rounds
    )
    self.secret_key=settings.jwt_secret_key
    self.algorithm=settings.jwt_algorithm
    self.access_token_expire_minutes = settings.jwt_access_token_expire_minutes
    
  def hash_passwords(self, password:str) -> str:
    return self.pwd_context.hash(password)
  
  def verify_password(self, plain_password:str, hashed_password:str) ->bool:
    return self.pwd_context.verify(plain_password,hashed_password)
  
  def create_access_token(
    self,
    data:dict,
    expires_delta: Optional[timedelta] = None
  ) -> str:
    to_encode = data.copy()
    if expires_delta:
      expire = datetime.now(timezone.utc) + expires_delta
    else:
      expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(
      to_encode,
      self.secret_key,
      algorithm=self.algorithm
    )
    return encoded_jwt
  
  def verify_token(self, token:str) -> Optional[dict]:
    try:
      payload=jwt.decode(
        token,
        self.secret_key,
        algorithms=[self.algorithm]
      )
      return payload
    except JWTError:
      return None
  def create_token_for_doctor(self, doctor_id:int, username:str)->str:
    token_data={
      "sub":username,
      "doctor_id":doctor_id,
      "type":"access_token"
    }
    return self.create_access_token(data=token_data)
  
auth_service = AuthService()
    