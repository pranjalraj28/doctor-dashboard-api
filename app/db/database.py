from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import (
  AsyncEngine,
  AsyncSession,
  async_sessionmaker,
  create_async_engine,
)
from sqlalchemy.pool import NullPool
from app.core.config import settings
from sqlalchemy.orm import declarative_base

class DatabaseManager:
  def __init__(self):
    self.engine: Optional[AsyncEngine] = None
    self.session_factory: Optional[async_sessionmaker[AsyncSession]] = None
    self.Base = declarative_base()
    
    
  def init_db(self) -> None:
    self.engine = create_async_engine(
      settings.database_url,
      poolclass = NullPool,
      echo = settings.debug,
      future = True
    )
    self.session_factory = async_sessionmaker(
      bind = self.engine,
      class_ = AsyncSession,
      expire_on_commit = False,
      autocommit = False,
      autoflush = False
    )
    
  async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
    if not self.session_factory:
      raise RuntimeError("Database not initialized. Call init_db() first.")
    
    async with self.session_factory() as session:
      try:
        yield session
      except Exception as e:
        await session.rollback()
        raise e
      finally:
        await session.close()
        
  async def close(self) -> None:
    if self.engine:
      await self.engine.dispose()
      
db_manager = DatabaseManager()
      
    
  
