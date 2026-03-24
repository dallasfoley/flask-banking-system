from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DBNAME = "banking_db"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}