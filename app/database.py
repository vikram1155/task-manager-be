from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://markiv1155:uYtcWllGBy3NSdGf@taskmanagerdb.q8uso.mongodb.net/?retryWrites=true&w=majority&appName=TaskManagerDB"

client = AsyncIOMotorClient(MONGO_URI)
db = client["TaskManagerDB"]  # Database Name

team_members_collection = db.get_collection("teamMembers")
tasks_collection = db.get_collection("allTasks")
users_collection = db.get_collection("users")
