from fastapi import FastAPI,Path, HTTPException 
from typing import Optional
from pydantic import BaseModel 
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId 

app = FastAPI()


client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["fast_db"]   # database name
collection = db["users"]  #collection name
stu_collection = db["students"]
updatestu_collection = db["updatestudents"]



class User(BaseModel):
    name:str 
    email:str  


class Student(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str]=None
    age: Optional[int]=None
    year: Optional[str]=None 


@app.post('/create/')
async def create_user(user: User):
    new_user = await collection.insert_one(user.dict())
    return {"id": str(new_user.inserted_id)}


@app.post("/create-student/")
async def create_student(student:Student):
    new_student = await stu_collection.insert_one(student.dict())
    return {"id": str(new_student.inserted_id)}


@app.put("/update-student/{student_id}")
async def update_student(student_id: str, student: Student):
    # Convert string ID to MongoDB ObjectId
    try:
        obj_id = ObjectId(student_id)  
    except:
        raise HTTPException(status_code=400, detail="Invalid student ID format")

    update_result = await updatestu_collection.update_one(
        {"_id": obj_id},  # Use ObjectId for searching
        {"$set": student.dict()}  # Update fields
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student updated successfully"}

# async def update_student(student_id:str, student:Student):
#     # update_student = await updatestu_collection.update_one(student.dict())
#     # return {"id": str(update_student.updated_id)}

#     update_result = await updatestu_collection.update_one(
#         {"_id": student_id},  # Find student by ID
#         {"$set": student.dict()}  # Update fields
#     )
#     if update_result.matched_count == 0:
#         raise HTTPException(status_code=404, detail="Student not found")
#     return {"message": "Student updated successfully"}


@app.get("/users/")
async def get_users():
    users = await collection.find().to_list(100)
    return [{"id": str(user["_id"]), "name": user["name"], "email": user["email"]} for user in users]

@app.get("/students/")
async def get_students():
    students = await stu_collection.find().to_list(100)
    return [{"id": str(student["_id"]), "name": student["name"], "age": student["age"],"year": student["year"]} for student in students]


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/students/{student_id}")
async def get_student(student_id: str):
    student = await stu_collection.find_one({"_id": ObjectId(student_id)})
    if student:
        return {"id": str(student["_id"]), "name": student["name"], "age": student["age"], "year": student["year"]}
    raise HTTPException(status_code=404, detail="student not found")    


@app.get("/")
def index():
    return {"name":"First Data"}



# @app.get("/get-by-name/{student_id}")
# def get_student(*, student_id:int,name: Optional[str]=None,test:int):
#     for student_id in students:
#         if students[student_id]["name"] == name:
#             return students[student_id]
#     return {"Data":"not found"}    

















# @app.put("/update-student/{student_id}")
# def update_student(student_id:int, student:UpdateStudent):
#     if student_id not in students:
#         return{"Error":"Student does not exist"}
    
#     if student.name != None:
#         students[student_id].name = student.name 

#     if student.age!=None:
#         students[student_id].age = student.age 

#     if student.year!=None:
#         students[student_id].year=student.year 

#     return students[student_id]
            

# @app.delete("/delete-student/{student_id}")
# def delete_student(student_id:int):
#     if student_id not in students:
#         return {"Error":"Student does not exist"}
    
#     del students[student_id]
#     return {"Message":"Student deleted successfully"}
    