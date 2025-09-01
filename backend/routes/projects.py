from flask import Blueprint

projects_blueprint = Blueprint("projects", __name__)

def list_projects():
    pass

def create_project():
    pass

def get_project(project_id: str):
    pass

def get_members(project_id: str):
    pass

def delete_project(project_id: str):
    pass

def join_project(project_code: str):
    pass

def create_task():
    pass

def get_task(project_id: str, task_id: str):
    pass

def edit_task(project_id: str, task_id: str):
    pass

def change_task_status(project_id: str, task_id: str):
    pass

def assign_task(project_id: str, task_id: str):
    pass

projects_blueprint.add_url_rule("/", endpoint="list-projects", view_func=list_projects, methods=["GET"])
projects_blueprint.add_url_rule("/", endpoint="create-project", view_func=create_project, methods=["POST"])
projects_blueprint.add_url_rule("/{project_id}", endpoint="get-project", view_func=get_project, methods=["GET"])
projects_blueprint.add_url_rule("/{project_id}", endpoint="delete-project", view_func=delete_project, methods=["DELETE"])
projects_blueprint.add_url_rule("/{project_id}/members", endpoint="get-project-members", view_func=get_members, methods=["GET"])

projects_blueprint.add_url_rule("/join/code/{project_code}", endpoint="join-project", view_func=join_project, methods=["POST"])

projects_blueprint.add_url_rule("/{project_id}/tasks", endpoint="create-project-task", view_func=create_task, methods=["POST"])
projects_blueprint.add_url_rule("/{project_id}/tasks/{task_id}", endpoint="get-task", view_func=get_task, methods=["GET"])
projects_blueprint.add_url_rule("/{project_id}/tasks/{task_id}", endpoint="edit-project-task", view_func=edit_task, methods=["PUT"])
projects_blueprint.add_url_rule("/{project_id}/tasks/{task_id}/status", endpoint="change-project-task-status", view_func=change_task_status, methods=["PUT"])
projects_blueprint.add_url_rule("/{project_id}/tasks/{task_id}/assign", endpoint="assign-project-task", view_func=assign_task, methods=["PUT"])