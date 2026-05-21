from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class DBSettings(BaseSettings):
    username: str
    password: str
    database: str
    host: str
    port: str

    class Config:
        env_prefix = "DB_"
        env_file_encoding = 'utf-8'
        extra = "ignore"
    def sync_url(self):
        return f"postgresql+psycopg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
