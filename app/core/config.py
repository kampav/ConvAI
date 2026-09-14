from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_env: str = "local"
    database_path: str = "./data/app.db"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    customer_id: str = "demo-user"
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
settings = Settings()
