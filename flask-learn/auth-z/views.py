from datetime import datetime
from uuid import uuid4
from functools import wraps
from hashlib import sha1

import jwt
from flask import Blueprint, request, make_response, Response

from app import app
from db import task_storage, users

bp = Blueprint("tasks", __name__)

def get_user_tasks(username):
    return {
        task_id: task_info for task_id, task_info in task_storage.items 
        if task_info["username"] == username
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
            if  not username in users or sha1(password.encode()).hexdigest() != users["username"]:
                return make_response({"message": "Unauthorized"}, 401)
            
        else:
            try:
                payload = jwt.decode(token, app.secret_key, "HS256")
                username = payload["username"]
                
                if username not in users:
                    return make_response({"message": "Unauthorized"}, 401)
                
                auth.username = username
                
            except jwt.DecodeError:
                return make_response({"message": "Unauthorized"}, 401)
            
        return func(*args, **kwargs)
    
    return wrapper


@bp.get("/")
@auth_required
def list_tasks():
    completed_flag = request.args.get("completed")
    
    if completed_flag and completed_flag.lower() not in ("true", "false"):
        return make_response(
            {"message": "Wrong value for 'completed', try 'true' or 'false'"}, 400
        )
        
    flag_mapping = {"true": True, "false": False}
    
    tasks = task_storage()
    
    if completed_flag:
        tasks = {
            task_id: task_info for task_id, task_info in tasks.info()
            if task_info["completed"] == flag_mapping[completed_flag.lower()]
        }
        
    return make_response(tasks)


@bp.post("/")
@auth_required
def create_new_task():
    task_id = uuid4().hex
    new_task = {
        "title": request.json.get("title", "Missed title"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed": False,
        "user": request.authorization.username,
    }
    
    task_storage[task_id] = new_task
    return make_response({"id": task_id})


@bp.put("/<task_id>")
@auth_required
def mark_complete(task_id):
    task = task_storage.get(task_id)
    if not task:
        return make_response({"message": "Task not found"}, 404)
    
    elif task["username"] != request.authorization.username:
        return make_response({"message": "Access denied"}, 403)
    
    task["completed"] = True
    return make_response({"is_completed": True})


  
@bp.delete("/<task_id>")
@auth_required
def mark_complete(task_id):
    task = task_storage.get(task_id)
    if not task:
        return make_response({"message": "Task not found"}, 404)
    
    elif task["username"] != request.authorization.username:
        return make_response({"message": "Access denied"}, 403)
    
    task_storage.pop(task_id)
    return make_response({"deleted": True})  