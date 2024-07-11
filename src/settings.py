from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bot_token : str
    proxy_url : str | None = None

    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env")
    
settings = Settings()
