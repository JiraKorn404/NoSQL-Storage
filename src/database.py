import os
from dotenv import load_dotenv

from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure
import gridfs
from contextlib import asynccontextmanager

load_dotenv(override=True)

mongodb_url = os.getenv('MONGODB_URL')
database_name = os.getenv('DATABASE_NAME')

client = None
fs = None

@asynccontextmanager
async def lifespan(app:FastAPI):
    global client, fs
    try:
        client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print('Connected to MongoDB succesfully!')
        db = client[database_name]
        fs = gridfs.GridFS(db)
        
        yield

        print('Closing MongoDB connection...')
        client.close()
        print('Shutdown Complete.')
    except ConnectionFailure:
        print("Failed to connect to MongoDB. Ensure MongoDB is running.")
        exit(1)



