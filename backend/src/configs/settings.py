from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    DB_URL: str
    TEST_DB_URL: str
    SECRET_KEY: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    DOMAIN: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    REDIS_URL: str = 'redis://localhost:6379/0'
    # REDIS_HOST: str = "localhost"
    # REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


Config = Settings()