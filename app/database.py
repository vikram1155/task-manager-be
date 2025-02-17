import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv("DATABASE_URL")

# Connect to the database
client = AsyncIOMotorClient(MONGO_URI)
db = client["TaskManagerDB"]

# Collections
team_members_collection = db.get_collection("teamMembers")
tasks_collection = db.get_collection("allTasks")
users_collection = db.get_collection("users")