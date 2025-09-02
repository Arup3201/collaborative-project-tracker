from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.exc import OperationalError, IntegrityError

from db import Database
from utils.id import generate_id
from models import Project, User, Membership, Task
from models.membership import Role
from models.project import TaskStatus
from exceptions import DBOverloadError, DBIntegrityError, NotFoundError, AlreadyExistError
from exceptions.project import NotProjectMemberError, NotProjectOwner

class ProjectService:
    def __init__(self):
        self.session = Database().get_session()

    def list_projects(self, user_id):
        project_list = []
        try:
            with self.session() as session:
                projects = session.query(Project, Membership).filter(and_(Project.id==Membership.project_id, Membership.user_id==user_id)).all()
                for project, member in projects:
                    project_list.append({
                        "id": project.id, 
                        "name": project.name, 
                        "description": project.description, 
                        "deadline": project.deadline, 
                        "code": project.code, 
                        "role": member.role.value, 
                        "created_at": project.created_at.strftime("%Y-%m-%d %I-%M-%S %p")
                    })
                
                return project_list
        except OperationalError as e:
            print(str(e))
            raise DBOverloadError()

    def create_projects(self, name: str, description: str, deadline: datetime, user_id: str):
        project_id = generate_id("PROJECT_")
        project_code = generate_id(size=5)

        try:
            with self.session() as session:
                project_instance = Project(id=project_id, name=name, description=description, deadline=deadline, code=project_code)
                user = session.query(User).filter(User.id==user_id).first()
                if not user:
                    raise NotFoundError(f"User with id {user_id} not found")
                
                member = Membership(user_id=user.id, project_id=project_id, role=Role.Owner)

                session.add(project_instance)
                session.commit()

                session.add(member)
                session.commit()

                return {
                    "id": project_instance.id, 
                    "name": project_instance.name, 
                    "description": project_instance.description, 
                    "deadline": project_instance.deadline, 
                    "code": project_instance.code, 
                    "created_at": project_instance.created_at.strftime("%Y-%m-%d %I:%M:%S %p")
                }
        except OperationalError as e:
            print(str(e))
            raise DBOverloadError()
        except IntegrityError as e:
            print(str(e))
            raise DBIntegrityError()

    def get_project(self, project_id: str, user_id: str):
        try:
            with self.session() as session:
                project = session.get(Project, project_id)
                if not project:
                    raise NotFoundError(f"Project with id {project_id} not found")

                membership = session.query(Project, Membership).filter(and_(Project.id==Membership.project_id, Project.id==project_id, Membership.user_id==user_id)).first()
                if not membership:
                    raise NotProjectMemberError(f"User with id {user_id} is not a member of the project with id {project_id}")
                
                project_details = {
                    "id": project.id, 
                    "name": project.name, 
                    "description": project.description, 
                    "deadline": project.deadline, 
                    "created_at": project.created_at, 
                    "code": project.code, 
                    "role": membership[1].role.value, 
                    "tasks": []
                }

                tasks = session.query(Task).filter(Task.project_id==project_id).all()
                for task in tasks:
                    assignee = session.query(User).filter(User.id==task.assignee).first()
                    if not assignee:
                        raise 
                    
                    project_details["tasks"].append({
                        "id": task.id, 
                        "name": task.name, 
                        "description": task.description, 
                        "assignee": {
                            "id": assignee.id, 
                            "name": assignee.name, 
                            "email": assignee.email,
                        }, 
                        "status": task.status.value, 
                        "created_at": task.created_at, 
                    })

                return project_details
        except OperationalError as e:
            print(str(e))
            raise DBOverloadError()

    def get_members(self, project_id: str, user_id: str):
        members_list = []
        try:
            with self.session() as session:
                project = session.get(Project, project_id)
                if not project:
                    raise NotFoundError(f"Project with id {project_id} not found")

                project_membership = session.query(Project, Membership).filter(and_(Project.id==Membership.project_id, Project.id==project_id, Membership.user_id==user_id)).first()
                if not project_membership:
                    raise NotProjectMemberError(f"User with id {user_id} is not a member of the project with id {project_id}")

                project_members = session.query(Project, Membership).filter(and_(Project.id==Membership.project_id, Project.id==project_id)).all()
                for row in project_members:
                    member = row[1]
                    user = session.query(User).filter(User.id==member.user_id).first()
                    if not user:
                        raise Exception("ERROR: member has no corresponding user in the users table")
                    
                    members_list.append({
                        "id": user.id, 
                        "name": user.name, 
                        "email": user.email, 
                        "role": member.role.value
                    })
                
                return members_list, None
        except OperationalError as e:
            print(str(e))
            raise DBOverloadError()

    def delete_project(self, project_id: str, user_id: str):
        try:
            with self.session() as session:
                project = session.get(Project, project_id)
                if not project:
                    raise NotFoundError(f"Project with id {project_id} not found")
                
                project_membership = session.query(Project, Membership).filter(and_(Project.id==Membership.project_id, Project.id==project_id, Membership.user_id==user_id)).first()
                if not project_membership:
                    raise NotProjectMemberError(f"User with id {user_id} is not a member of the project with id {project_id}")

                if project_membership[1].role != Role.Owner:
                    raise NotProjectOwner(f"User with id {user_id} is not the owner of the project with id {project_id}")
                
                session.delete(project)
                session.commit()
        except OperationalError as e:
            print(str(e))
            raise DBOverloadError()

    def join_project(self, project_code: str, user_id: str):
        try:
            with self.session() as session:
                project = session.query(Project).filter(Project.code==project_code).first()
                if not project:
                    raise NotFoundError(f"Project code {project_code} is invalid")
                
                project_membership = session.query(Project, Membership).filter(and_(Project.id==Membership.project_id, Project.id==project.id, Membership.user_id==user_id)).first()
                if project_membership:
                    raise AlreadyExistError(f"User with id {user_id} is already a member of the project with id {project.id}")
                
                member = Membership(user_id=user_id, project_id=project.id, role=Role.Member)
                session.add(member)
                session.commit()
        except OperationalError as e:
            print(str(e))
            raise DBOverloadError()

    def create_task(self, name: str, description: str, assignee: str, status: TaskStatus, project_id: str, user_id: str):
        try:
            with self.session() as session:
                checking = session.query(Project).filter(Project.id==project_id).first()
                if not checking:
                    raise NotFoundError(f"Project with id {project_id} is not found")
                
                checking = session.query(User).filter(User.id==assignee).first()
                if not checking:
                    raise NotFoundError("assignee with id {assignee} does not exist")

                project_membership = session.query(Project, Membership).filter(and_(Project.id==Membership.project_id, Project.id==project_id, Membership.user_id==assignee)).first()
                if not project_membership:
                    raise NotProjectMemberError(f"User with id {user_id} is not a member of the project with id {project_id}")
                
                if project_membership[1].role != Role.Owner:
                    raise NotProjectOwner(f"User with id {user_id} is not the owner of the project with id {project_id}")
                
                task_id = generate_id("TASK_")
                task = Task(id=task_id, 
                            name=name, 
                            description=description, 
                            assignee=assignee, 
                            status=status, 
                            project_id=project_id)
                session.add(task)
                session.commit()

        except OperationalError as e:
            print(str(e))
            raise DBOverloadError()
    