from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    bot_token: str
    proxy_url: str | None = None

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] | None = "INFO"
    logging_format: str = "{log_color}{levelname} : {asctime} - {light_yellow}{name}{reset} : {message}{reset}"
    app_name: str = "post-tracker-bot"

    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env")


settings = Settings()
