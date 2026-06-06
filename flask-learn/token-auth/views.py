from functools import wraps
from hashlib import sha1
from uuid import uuid4
from datetime import datetime
import jwt

from flask import Blueprint, make_response, request

from db import task_storage, users
from app import app

bp = Blueprint("tasks", __name__)


def get_user_tasks(username):
    return {
        task_id: task_info for task_id, task_info in task_storage.items()
        if task_info['username'] == username
    }
    

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        
        if not auth:
            return make_response({"message": "Unauthorized"}, 401)
        
        username = auth.username
        password = auth.password
        token = auth.token
        
        if username and password:
            if username not in users or sha1(password.encode()).hexdigest() != users[username]:
                return make_response({"message": "Unauthorized"}, 401)
            
        else:
            try:
                payload = jwt.decode(token, app.secret_key, "HS256")
                username = payload["username"]
                
                if username not in users:
                    return make_response({"message": "Unauthorized"}, 401)
                
                auth.username = username
                
            except jwt.exceptions.DecodeError:
                return make_response({"message": "Unauthorized"}, 401)
        
        return func(*args, **kwargs)
    
    return wrapper


@bp.get("/")
@auth_required
def list_tasks():
    completed_flag = request.args.get("completed")  # fetch the query parameter
    # check that query parameter has valid value
    if completed_flag and completed_flag.lower() not in ("true", "false"):
        # say to a user that the request is invalid
        return make_response(
            {"message": "Wrong value for `completed`. Expected `true` or `false`."},
            400,
        )

    flag_mapping = {"true": True, "false": False}

    if not completed_flag:
        # return all tasks if query parameter was not provided
        tasks = get_user_tasks(request.authorization.username)
    else:
        # filter only not completed tasks
        tasks = {
            task_id: task_info for task_id, task_info in get_user_tasks(request.authorization.username).items()
            if task_info["is_completed"] == flag_mapping[completed_flag.lower()]
        }

    return make_response(tasks)  # return tasks


@bp.post("/")
@auth_required
def create_task():
    task_id = uuid4().hex  # generate task ID
    task_info = {
        "title": request.json.get("title", "Missed title"),  # get `title` from the request body
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # get current time
        "is_completed": False,  # by default a new task is not completed
        "username": request.authorization.username
    }

    task_storage[task_id] = task_info  # save the task in the storage

    return make_response({"id": task_id})  # return ID of the new task


@bp.put("/<task_id>")
@auth_required
def mark_completed(task_id):
    tasks = get_user_tasks(request.authorization.username)
    task = tasks.get(task_id)  # try to find task by the provided ID from the path
    if not task:
        # say to a user that the task with provided ID doesn't exist
        return make_response({"message": "Task not found"}, 404)

    task["is_completed"] = True  # mark the task as completed

    return make_response({"is_completed": True})


@bp.delete("/<task_id>")
@auth_required
def delete(task_id):
    tasks = get_user_tasks(request.authorization.username)
    task = task_storage.pop(task_id, None)  # try to delete task by the provided ID from the path
    if not task:
        # say to a user that the task with provided ID doesn't exist
        return make_response({"message": "Task not found"}, 404)

    return make_response({"deleted": True})
