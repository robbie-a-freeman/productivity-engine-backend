from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_task,
    delete_task,
    retrieve_task,
    retrieve_tasks,
    update_task,
)
from server.models.task import (
    ErrorResponseModel,
    ResponseModel,
    TaskSchema,
    UpdateTaskModel,
)

router = APIRouter()

# Create
@router.post("/", response_description="Task data added into the database")
async def add_task_data(task: TaskSchema = Body(...)):
    task = jsonable_encoder(task)
    new_task = await add_task(task)
    return ResponseModel(new_task, "Task added successfully.")

# Read
@router.get("/", response_description="Tasks retrieved")
async def get_tasks():
    tasks = await retrieve_tasks()
    if tasks:
        return ResponseModel(tasks, "Tasks data retrieved successfully")
    return ResponseModel(tasks, "Empty list returned")


@router.get("/{id}", response_description="Task data retrieved")
async def get_task_data(id):
    task = await retrieve_task(id)
    if task:
        return ResponseModel(task, "Task data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Task doesn't exist.")

# Update
@router.put("/{id}")
async def update_task_data(id: str, req: UpdateTaskModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_task = await update_task(id, req)
    if updated_task:
        return ResponseModel(
            "Task with ID: {} name update is successful".format(id),
            "Task name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the task data.",
    )

# Delete
@router.delete("/{id}", response_description="Task data deleted from the database")
async def delete_task_data(id: str):
    deleted_task = await delete_task(id)
    if deleted_task:
        return ResponseModel(
            "Task with ID: {} removed".format(id), "Task deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Task with id {0} doesn't exist".format(id)
    )