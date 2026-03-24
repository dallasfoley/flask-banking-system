import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI") # temporary debug line


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

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