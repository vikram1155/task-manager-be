from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Team Member Model
class TeamMember(BaseModel):
    name: str
    age: Optional[int]
    email: EmailStr
    phone: str  # 10-digit number
    role: str
    remarks: Optional[str]
    teamMemberId:str
    access: str

# Task Model
class Task(BaseModel):
    taskId: str
    title: str
    assignee: EmailStr
    description: str
    type: str
    assignedOn: str
    status: str
    assignedTo: EmailStr
    storyPoints: int
    comments: Optional[str]
    deadline: datetime
    priority: str

class User(BaseModel):
    name: str
    email: EmailStr
    password: str  # hashed password
    role: str
    age: int
    phone: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class UserSummary(BaseModel):
    name: str
    email: str
    role: str
    age: int
    phone: str
