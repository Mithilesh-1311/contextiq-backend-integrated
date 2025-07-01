from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///app.db"
    JWT_SECRET_KEY: str = "jwt-secret-key"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

