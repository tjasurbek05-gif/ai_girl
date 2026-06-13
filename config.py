from pydantic_settings import BaseSettings


class Config(BaseSettings):
    BOT_TOKEN: str
    BOT_USERNAME: str = "VelvetAIBot"
    DEEPSEEK_API_KEY: str
    MEDIA_CHANNEL_ID: int
    SUPER_ADMIN_ID: int
    DB_PATH: str = "velvet.db"

    DAILY_ENERGY: int = 49
    ENERGY_PER_MESSAGE: int = 1

    # Telegram Stars pricing
    PRICE_2DAYS: int = 89
    PRICE_1MONTH: int = 199
    PRICE_3MONTHS: int = 449
    PRICE_1YEAR: int = 1499

    # Gems bundled with each plan
    GEMS_2DAYS: int = 20
    GEMS_1MONTH: int = 30
    GEMS_3MONTHS: int = 70
    GEMS_1YEAR: int = 210

    class Config:
        env_file = ".env"


config = Config()
