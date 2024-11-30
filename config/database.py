from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    logging.info("Connected to MongoDB successfully.")
except Exception as e:
    logging.error("Failed to connect to MongoDB:", exc_info=True)
    raise RuntimeError("Failed to connect to MongoDB. Please check your configuration.") from e