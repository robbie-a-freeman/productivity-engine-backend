import motor.motor_asyncio
from bson.objectid import ObjectId
from datetime import datetime
from dateutil.parser import parse

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.tasks

task_collection = database.get_collection("tasks_collection")

# helpers

def task_helper(task) -> dict:

    return {
        "id": str(task["_id"]),
        "name": str(task["name"]),
        "last_completion": parse(task["last_completion"]),
        "days_between_completions": float(task["days_between_completions"]),
        "creation_date": parse(task["creation_date"])
    }

# Retrieve all tasks present in the database
async def retrieve_tasks():
    tasks = []
    async for task in task_collection.find():
        tasks.append(task_helper(task))
    return tasks


# Add a new task into to the database
async def add_task(task_data: dict) -> dict:
    task = await task_collection.insert_one(task_data)
    new_task = await task_collection.find_one({"_id": task.inserted_id})
    return task_helper(new_task)


# Retrieve a task with a matching ID
async def retrieve_task(id: str) -> dict:
    task = await task_collection.find_one({"_id": ObjectId(id)})
    if task:
        return task_helper(task)


# Update a task with a matching ID
async def update_task(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    task = await task_collection.find_one({"_id": ObjectId(id)})
    if task:
        updated_task = await task_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_task:
            return True
        return False


# Delete a task from the database
async def delete_task(id: str):
    task = await task_collection.find_one({"_id": ObjectId(id)})
    if task:
        await task_collection.delete_one({"_id": ObjectId(id)})
        return True