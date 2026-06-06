from uuid import uuid4
from datetime import datetime
from flask import Flask, make_response, request

app = Flask("TaskManager")

task_storage = {}


@app.route("/")
def list_tasks():
    tasks = task_storage
    completed_flag = request.args.get("completed", "")
    
    if completed_flag.lower() == "true":
        tasks = {
            task_id: task_info for task_id, task_info in tasks.items() if task_info["is_completed"]
        }
    elif completed_flag.lower() == "false":
        tasks = {
            task_id: task_info for task_id, task_info in tasks.items() if not task_info["is_completed"]
        }
        
    return make_response(tasks)


@app.post("/")
def create_task():
    task_id = uuid4().hex
    new_task = {
        "title": request.json.get("title", "Missed title"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "is_completed": False,
    }
    task_storage[task_id] = new_task
    return make_response({"id": task_id})


@app.put("/<task_id>")
def mark_completed(task_id):
    task = task_storage.get(task_id)
    if not task:
        return make_response(({"message": "Task not found"}, 404))
    
    task["is_completed"] = True
    
    return make_response({"is_completed": True})


@app.delete("/<task_id>")
def delete_task(task_id):
    task = task_storage.pop(task_id, None)
    if not task:
        return make_response(({"message": "Task not found"}, 404))
    
    return make_response({"deleted": True})


if __name__ == "__main__":
    app.run(debug=True)