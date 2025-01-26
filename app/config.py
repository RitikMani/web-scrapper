from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_TOKEN: str = "ritik123"
    PROXY_URL: str = ""
    MAX_RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 5  # seconds

settings = Settings()