from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # APP
    PROJECT_NAME: str
    DEBUG: bool
    ENVIRONMENT: str
    # DATABASE
    DB_USER: str
    DB_PWD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str

    # SECURITY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: float
    SECRET_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    def ENVIRONMET(self) -> str:
        return f"{self.ENVIRONMENT}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings() # type: ignore 