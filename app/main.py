from fastapi import FastAPI, HTTPException
from app.database import team_members_collection, tasks_collection, users_collection
from app.models import TeamMember, Task, User, LoginRequest, UserSummary
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import List
from bson import ObjectId
from fastapi import HTTPException
from passlib.context import CryptContext


logging.basicConfig(level=logging.ERROR)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# success response
def success_response(data=None, message="success"):
    return {
        "data": data,
        "status": {
            "code": 200,
            "message": message
        }
    }

# error response
def error_response(message="error", code=400):
    logging.error(f"Error {code}: {message}") 
    raise HTTPException(status_code=code, detail={"message": message})

@app.get("/")
async def home():
    return success_response({"message": "MongoDB Connected Successfully"})

# Logn/Signup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Signup API
@app.post("/signup/")
async def signup(user: User):
    existing_user = await users_collection.find_one({"email": user.email})
    print("Existing user found:", existing_user)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password

    # Insert user into DB
    result = await users_collection.insert_one(user_dict)

    # Return user details without password
    user_details = {
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "phone": user.phone,
        "age": user.age
    }

    return success_response({"userDetails": user_details}, "User Created")


# Login API
@app.post("/login/")
async def login(request: LoginRequest):
    user = await users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify hashed password
    if not pwd_context.verify(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    return success_response({"userDetails": {"name": user["name"], "email": user["email"], "role": user["role"], "phone":user["phone"], "age": user["age"]}}, "User Logged in")

# Get Users    
@app.get("/allusers/", response_model=List[UserSummary])
async def get_users():
    try:
        users = await users_collection.find({}, {"name": 1, "email": 1, "role": 1, "age": 1, "phone": 1, "_id": 0}).to_list(100)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Task
# Create
@app.post("/allTasks/")
async def create_task(task: Task):
    try:
        result = await tasks_collection.insert_one(task.dict())  
        return success_response({"id": str(result.inserted_id)}, "Task Created")
    except Exception as e:
        error_response(str(e), 500)

# Read
@app.get("/allTasks/", response_model=List[Task])
async def get_tasks():
    tasks = await tasks_collection.find().to_list(100)
    return tasks

# Update
@app.put("/allTasks/{task_id}")
async def update_task(task_id: str, task: Task):
    try:
        from uuid import UUID
        try:
            UUID(task_id, version=4)
        except ValueError:
            return error_response("Invalid task ID format", 400)

        updated_task = await tasks_collection.update_one(
            {"taskId": task_id}, {"$set": task.dict()}
        )

        if updated_task.matched_count == 0:
            return error_response("Task not found", 404)

        return success_response("Task Updated Successfully")
    except Exception as e:
        return error_response(str(e), 500)

# Delete
@app.delete("/allTasks/{task_id}")
async def delete_task(task_id: str):
    try:
        from uuid import UUID
        try:
            UUID(task_id, version=4)
        except ValueError:
            return error_response("Invalid task ID format", 400)

        deleted_task = await tasks_collection.delete_one(
            {"taskId": task_id}
        )

        if deleted_task.deleted_count == 0:
            return error_response("Task not found", 404)

        return success_response("Task Deleted Successfully")
    except Exception as e:
        return error_response(str(e), 500)


# Team Member
# Create
@app.post("/teamMembers/")
async def create_team_member(team_member: TeamMember):
    try:
        existing_member = await team_members_collection.find_one({"email": team_member.email})
        if existing_member:
            return error_response("Email already exists", 400)

        result = await team_members_collection.insert_one(team_member.dict())
        return success_response({"id": str(result.inserted_id)}, "Team Member Added")
    except Exception as e:
        error_response(str(e), 500)


# Read
@app.get("/teamMembers/", response_model=List[TeamMember])
async def get_team_members():
    members = await team_members_collection.find().to_list(100)
    return members

# Update
@app.put("/teamMembers/{team_member_id}")
async def update_team_member(team_member_id: str, team_member: TeamMember):
    try:
        from uuid import UUID
        try:
            UUID(team_member_id, version=4)
        except ValueError:
            return error_response("Invalid team member ID format", 400)
        
        updated_team_member = await team_members_collection.update_one(
            {"teamMemberId": team_member_id}, {"$set": team_member.dict()}
        )

        if updated_team_member.matched_count == 0:
            return error_response("Team member not found", 404)

        return success_response("Team Member Updated Successfully")
    except Exception as e:
        return error_response(str(e), 500)

# Delete
@app.delete("/teamMembers/{team_member_id}")
async def delete_task(team_member_id: str):
    try:
        from uuid import UUID
        try:
            UUID(team_member_id, version=4)
        except ValueError:
            return error_response("Invalid task ID format", 400)

        deleted_team_member = await team_members_collection.delete_one(
            {"teamMemberId": team_member_id}
        )

        if deleted_team_member.deleted_count == 0:
            return error_response("Task not found", 404)

        return success_response("Task Deleted Successfully")
    except Exception as e:
        return error_response(str(e), 500)