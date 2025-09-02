from flask import Blueprint, request, jsonify
import pydantic

from validation.payload import CreateProjectPayload, CreateTaskPayload
from validation.user import User
from services.project import ProjectService
from exceptions import DBOverloadError, DBIntegrityError, NotFoundError, AlreadyExistError
from exceptions.project import NotProjectMemberError, NotProjectOwner

projects_blueprint = Blueprint("projects", __name__)

def list_projects():
    try:
        user = User(**request.environ["user"])
    except pydantic.ValidationError as e:
        errors = []
        for err in e.errors():
            errors.append({
                "message": err["msg"], 
                "input": err["input"], 
                "loc": err["loc"]
            })
        print(errors)
        return jsonify({
            "error": {
                "message": "Invalid user data",
                "details": "User data saved at server is corrupted",  
                "code": "SERVER_FAILURE"
            }
        }), 500

    try:
        projects = ProjectService().list_projects(user_id=user.id)
        return jsonify({
            "message": "fetched all projects", 
            "data": projects
        })
    except DBOverloadError as e:
        return jsonify({
            "error": {
                "message": "Server is overloaded",
                "details": str(e),  
                "code": "SERVER_FAILURE"
            }
        }), 500
    except Exception as e:
        print(e)
        return jsonify({
            "error": {
                "message": "Unknown server error occured",
                "details": "We are working on the server, please try again later",  
                "code": "SERVER_FAILURE"
            }
        }), 500

def create_project():
    try:
        payload = CreateProjectPayload(**request.get_json())
    except pydantic.ValidationError as e:
        errors = []
        for err in e.errors():
            errors.append({
                "message": err["msg"], 
                "input": err["input"], 
                "loc": err["loc"]
            })

        return jsonify({
            "error": {
                "message": "Input validation failed",
                "details": "Please make sure your input has required fields with their correct type",  
                "errors": errors, 
                "code": "BAD_REQUEST"
            }
        }), 400

    if not payload.name:
        return jsonify({
            "error": {
                "message": "Invalid project name",
                "details": "Field 'name' in project can't be empty",  
                "code": "BAD_REQUEST"
            }
        }), 400
    if not payload.deadline:
        return jsonify({
            "error": {
                "message": "Invalid project deadline",
                "details": "Field 'deadline' in project can't be empty",  
                "code": "BAD_REQUEST"
            }
        }), 400

    try:
        user = User(**request.environ["user"])
    except pydantic.ValidationError as e:
        errors = []
        for err in e.errors():
            errors.append({
                "message": err["msg"], 
                "input": err["input"], 
                "loc": err["loc"]
            })
        print(errors)
        return jsonify({
            "error": {
                "message": "Invalid user data",
                "details": "User data saved at server is corrupted",  
                "code": "SERVER_FAILURE"
            }
        }), 500

    try:
        project = ProjectService().create_projects(name=payload.name, description=payload.description, deadline=payload.deadline, user_id=user.id)
        return jsonify({
            "message": "project created", 
            "data": project, 
        })
    except NotFoundError as e:
        return jsonify({
            "error": {
                "message": "Value not found",
                "details": str(e),  
                "code": "NOT_FOUND"
            }
        }), 404
    except DBIntegrityError as e:
        return jsonify({
            "error": {
                "message": str(e),
                "details": "While creating membership and project intance, integrity error happened",  
                "code": "SERVER_FAILURE"
            }
        }), 500
    except DBOverloadError as e:
        return jsonify({
            "error": {
                "message": "Server is overloaded",
                "details": str(e),  
                "code": "SERVER_FAILURE"
            }
        }), 500
    except Exception as e:
        print(str(e))
        return jsonify({
            "error": {
                "message": "Something went wrong in the server",
                "details": "We are working on the error, please try again later",  
                "code": "SERVER_FAILURE"
            }
        }), 500

def get_project(project_id: str):
    try:
        user_payload = User(**request.environ["user"])
    except pydantic.ValidationError as e:
        errors = []
        for err in e.errors():
            errors.append({
                "message": err["msg"], 
                "input": err["input"], 
                "loc": err["loc"]
            })
        print(errors)
        return jsonify({
            "error": {
                "message": "Invalid user data",
                "details": "User data saved at server is corrupted",  
                "code": "SERVER_FAILURE"
            }
        }), 500
    
    try:
        project_details = ProjectService().get_project(project_id=project_id, user_id=user_payload.id)
        return jsonify({
            "message": f"project {project_id} fetched", 
            "data": project_details
        })
    except NotProjectMemberError as e:
        return jsonify({
            "error": {
                "message": "User is not a project member",
                "details": str(e),  
                "code": "NOT_MEMBER"
            }
        }), 400
    except NotFoundError as e:
        return jsonify({
            "error": {
                "message": "Value not found",
                "details": str(e),  
                "code": "NOT_FOUND"
            }
        }), 404
    except DBOverloadError as e:
        return jsonify({
            "error": {
                "message": "Server is overloaded",
                "details": str(e),  
                "code": "SERVER_FAILURE"
            }
        }), 500
    except Exception as e:
        print(str(e))
        return jsonify({
            "error": {
                "message": "Something went wrong in the server",
                "details": "We are working on the error, please try again later",  
                "code": "SERVER_FAILURE"
            }
        }), 500

def get_members(project_id: str):
    try:
        user_payload = User(**request.environ["user"])
    except pydantic.ValidationError as e:
        errors = []
        for err in e.errors():
            errors.append({
                "message": err["msg"], 
                "input": err["input"], 
                "loc": err["loc"]
            })
        print(errors)
        return jsonify({
            "error": {
                "message": "Invalid user data",
                "details": "User data saved at server is corrupted",  
                "code": "SERVER_FAILURE"
            }
        }), 500

    try:
        members, err = ProjectService().get_members(project_id=project_id, user_id=user_payload.id)
        return jsonify({
            "message": "members fetched", 
            "data": members
        })
    except NotProjectMemberError as e:
        return jsonify({
            "error": {
                "message": "User is not a project member",
                "details": str(e),  
                "code": "NOT_MEMBER"
            }
        }), 400
    except NotFoundError as e:
        return jsonify({
            "error": {
                "message": "Value not found",
                "details": str(e),  
                "code": "NOT_FOUND"
            }
        }), 404
    except DBOverloadError as e:
        return jsonify({
            "error": {
                "message": "Server is overloaded",
                "details": str(e),  
                "code": "SERVER_FAILURE"
            }
        }), 500
    except Exception as e:
        print(str(e))
        return jsonify({
            "error": {
                "message": "Something went wrong in the server",
                "details": "We are working on the error, please try again later",  
                "code": "SERVER_FAILURE"
            }
        }), 500

def delete_project(project_id: str):
    try:
        user_payload = User(**request.environ["user"])
    except pydantic.ValidationError as e:
        errors = []
        for err in e.errors():
            errors.append({
                "message": err["msg"], 
                "input": err["input"], 
                "loc": err["loc"]
            })
        print(errors)
        return jsonify({
            "error": {
                "message": "Invalid user data",
                "details": "User data saved at server is corrupted",  
                "code": "SERVER_FAILURE"
            }
        }), 500

    try:
        ProjectService().delete_project(project_id=project_id, user_id=user_payload.id)
        return jsonify({
            "message": "project deleted", 
        })
    except NotProjectMemberError as e:
        return jsonify({
            "error": {
                "message": "User is not a project member",
                "details": str(e),  
                "code": "NOT_MEMBER"
            }
        }), 400
    except NotProjectOwner as e:
        return jsonify({
            "error": {
                "message": "User is not the project owner",
                "details": str(e),  
                "code": "NOT_OWNER"
            }
        }), 400
    except NotFoundError as e:
        return jsonify({
            "error": {
                "message": "Value not found",
                "details": str(e),  
                "code": "NOT_FOUND"
            }
        }), 404
    except DBOverloadError as e:
        return jsonify({
            "error": {
                "message": "Server is overloaded",
                "details": str(e),  
                "code": "SERVER_FAILURE"
            }
        }), 500
    except Exception as e:
        print(str(e))
        return jsonify({
            "error": {
                "message": "Something went wrong in the server",
                "details": "We are working on the error, please try again later",  
                "code": "SERVER_FAILURE"
            }
        }), 500

def join_project(project_code: str):
    try:
        user_payload = User(**request.environ["user"])
    except pydantic.ValidationError as e:
        errors = []
        for err in e.errors():
            errors.append({
                "message": err["msg"], 
                "input": err["input"], 
                "loc": err["loc"]
            })
        print(errors)
        return jsonify({
            "error": {
                "message": "Invalid user data",
                "details": "User data saved at server is corrupted",  
                "code": "SERVER_FAILURE"
            }
        }), 500

    try:
        ProjectService().join_project(project_code=project_code, user_id=user_payload.id)
        return jsonify({
            "message": "You have joined the project as a member", 
        })
    except AlreadyExistError as e:
        return jsonify({
            "error": {
                "message": "User is already a member",
                "details": str(e),  
                "code": "ALREADY_MEMBER"
            }
        }), 400
    except NotProjectMemberError as e:
        return jsonify({
            "error": {
                "message": "User is not a project member",
                "details": str(e),  
                "code": "NOT_MEMBER"
            }
        }), 400
    except NotFoundError as e:
        return jsonify({
            "error": {
                "message": "Value not found",
                "details": str(e),  
                "code": "NOT_FOUND"
            }
        }), 404
    except DBOverloadError as e:
        return jsonify({
            "error": {
                "message": "Server is overloaded",
                "details": str(e),  
                "code": "SERVER_FAILURE"
            }
        }), 500
    except Exception as e:
        print(str(e))
        return jsonify({
            "error": {
                "message": "Something went wrong in the server",
                "details": "We are working on the error, please try again later",  
                "code": "SERVER_FAILURE"
            }
        }), 500

def create_task(project_id: str):
    try:
        payload = CreateTaskPayload(**request.get_json())
    except pydantic.ValidationError as e:
        errors = []
        for err in e.errors():
            errors.append({
                "message": err["msg"], 
                "input": err["input"], 
                "loc": err["loc"]
            })

        return jsonify({
            "error": {
                "message": "Input validation failed",
                "details": "Please make sure your input has required fields with their correct type",  
                "errors": errors, 
                "code": "BAD_REQUEST"
            }
        }), 400

    if not payload.name:
        return jsonify({
            "error": {
                "message": "Invalid task name",
                "details": "Field 'name' in task can't be empty",  
                "code": "BAD_REQUEST"
            }
        }), 400
    if not payload.assignee:
        return jsonify({
            "error": {
                "message": "Invalid task assignee",
                "details": "Field 'assignee' in task can't be empty",  
                "code": "BAD_REQUEST"
            }
        }), 400

    try:
        user_payload = User(**request.environ["user"])
    except pydantic.ValidationError as e:
        errors = []
        for err in e.errors():
            errors.append({
                "message": err["msg"], 
                "input": err["input"], 
                "loc": err["loc"]
            })
        print(errors)
        return jsonify({
            "error": {
                "message": "Invalid user data",
                "details": "User data saved at server is corrupted",  
                "code": "SERVER_FAILURE"
            }
        }), 500

    try:
        ProjectService().create_task(name=payload.name, 
                                     description=payload.description, 
                                     assignee=payload.assignee, 
                                     status=payload.status, 
                                     project_id=project_id, 
                                     user_id=user_payload.id)
        return jsonify({
            "message": "Task is created", 
        })
    except NotProjectMemberError as e:
        return jsonify({
            "error": {
                "message": "User is not a project member",
                "details": str(e),  
                "code": "NOT_MEMBER"
            }
        }), 400
    except NotProjectOwner as e:
        return jsonify({
            "error": {
                "message": "User is not a project owner",
                "details": str(e),  
                "code": "NOT_OWNER"
            }
        }), 400
    except NotFoundError as e:
        return jsonify({
            "error": {
                "message": "Value not found",
                "details": str(e),  
                "code": "NOT_FOUND"
            }
        }), 404
    except DBOverloadError as e:
        return jsonify({
            "error": {
                "message": "Server is overloaded",
                "details": str(e),  
                "code": "SERVER_FAILURE"
            }
        }), 500
    except Exception as e:
        print(str(e))
        return jsonify({
            "error": {
                "message": "Something went wrong in the server",
                "details": "We are working on the error, please try again later",  
                "code": "SERVER_FAILURE"
            }
        }), 500

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