from flask import Blueprint, request, jsonify

from validation.payload import CreateProjectPayload
from validation.user import User
from services.project import ProjectService

projects_blueprint = Blueprint("projects", __name__)

def list_projects():
    user = User(**request.environ["user"])
    projects = ProjectService().list_projects(user_id=user.id)
    return jsonify({
        "message": "fetched all projects", 
        "data": projects
    })

def create_project():
    payload = CreateProjectPayload(**request.get_json())

    user_payload = User(**request.environ["user"])
    project = ProjectService().create_projects(name=payload.name, description=payload.description, deadline=payload.deadline, user_id=user_payload.id)
    return jsonify({
        "message": "project created", 
        "data": project, 
    })

def get_project(project_id: str):
    user_payload = User(**request.environ["user"])
    project_details = ProjectService().get_project(project_id=project_id, user_id=user_payload.id)
    return jsonify({
        "message": f"project {project_id} fetched", 
        "data": project_details
    })

def get_members(project_id: str):
    user_payload = User(**request.environ["user"])
    members, err = ProjectService().get_members(project_id=project_id, user_id=user_payload.id)
    if err:
        return jsonify({
            "message": "FETCH_ERROR", 
            "error": err, 
            "code": 400
        }, 400)

    return jsonify({
        "message": "members fetched", 
        "data": members
    })

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
projects_blueprint.add_url_rule("/<project_id>", endpoint="get-project", view_func=get_project, methods=["GET"])
projects_blueprint.add_url_rule("/<project_id>", endpoint="delete-project", view_func=delete_project, methods=["DELETE"])
projects_blueprint.add_url_rule("/<project_id>/members", endpoint="get-project-members", view_func=get_members, methods=["GET"])

projects_blueprint.add_url_rule("/join/code/<project_code>", endpoint="join-project", view_func=join_project, methods=["POST"])

projects_blueprint.add_url_rule("/<project_id>/tasks", endpoint="create-project-task", view_func=create_task, methods=["POST"])
projects_blueprint.add_url_rule("/<project_id>/tasks/<task_id>", endpoint="get-task", view_func=get_task, methods=["GET"])
projects_blueprint.add_url_rule("/<project_id>/tasks/<task_id>", endpoint="edit-project-task", view_func=edit_task, methods=["PUT"])
projects_blueprint.add_url_rule("/<project_id>/tasks/<task_id>/status", endpoint="change-project-task-status", view_func=change_task_status, methods=["PUT"])
projects_blueprint.add_url_rule("/<project_id>/tasks/<task_id>/assign", endpoint="assign-project-task", view_func=assign_task, methods=["PUT"])