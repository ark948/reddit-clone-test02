from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    DB_URL: str
    SECRET_KEY: str
    REDIS_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


Config = Settings()


    # DB_URL: str
    # TEST_DB_URL: str
    # SECRET_KEY: str
    # REDIS_URL: str
    # JWT_SECRET: str
    # JWT_ALGORITHM: str
    # DOMAIN: str
    # TEST_PATH: str
