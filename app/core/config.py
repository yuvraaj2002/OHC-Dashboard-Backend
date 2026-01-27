from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    CLIENT_ID:str
    CLIENT_SECRET:str
    SESSION_SECRET_KEY:str
    SECRET_KET:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    FRONTEND_BASE_URL: str = "http://localhost:3000"  # Default frontend URL for verification links
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
        
settings = Settings()