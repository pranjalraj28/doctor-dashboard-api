from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  
  #Application
  app_name: str = "Doctor Dashboard API"
  app_version: str = "1.0.0"
  debug: bool = True
  api_v1_str: str = "/app/v1"
  database_url:str
  sync_database_url: str
  #jwt
  bcrypt_rounds: int = 12
  jwt_secret_key: str
  jwt_algorithm: str = "HS256"
  jwt_access_token_expire_minutes: int = 30
  
  class Config:
    env_file = ".env"
    case_sensitive = False
    
settings = Settings()
  