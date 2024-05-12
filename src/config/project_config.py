from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    DESCRIPTION: str


settings = Settings(
    PROJECT_NAME="Fitness Club",
    VERSION="0.1.0",
    DEBUG=True,
    DESCRIPTION="API for Fitness Club",
)
