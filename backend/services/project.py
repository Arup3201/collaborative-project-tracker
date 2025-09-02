from datetime import datetime
from sqlalchemy import and_

from db import Database
from utils.id import generate_id
from models import Project, User, Membership, Task
from models.membership import Role
from models.project import TaskStatus

class ProjectService:
    def __init__(self):
        self.session = Database().get_session()

    def list_projects(self, user_id):
        project_list = []
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

    def create_projects(self, name: str, description: str, deadline: datetime, user_id: str):
        project_id = generate_id("PROJECT_")
        project_code = generate_id(size=5)

        with self.session() as session:
            project_instance = Project(id=project_id, name=name, description=description, deadline=deadline, code=project_code)
            user = session.query(User).filter(User.id==user_id).first()
            if not user:
                return dict(), "user id not found"
            
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

    def get_project(self, project_id: str, user_id: str):
        with self.session() as session:
            project = session.get(Project, project_id)
            if not project:
                return None, "project does not exist"

            membership = session.query(Project, Membership).filter(and_(Project.id==Membership.project_id, Project.id==project_id, Membership.user_id==user_id)).first()
            if not membership:
                return None, "user is not part of this project"
            
            project_details = {
                "id": project.id, 
                "name": project.name, 
                "description": project.description, 
                "deadline": project.deadline, 
                "created_at": project.created_at, 
                "code": project.code, 
                "tasks": []
            }

            tasks = session.query(Task).filter(Task.project_id==project_id).all()
            for task in tasks:
                assignee = session.query(User).filter(User.id==task.assignee).first()
                if not assignee:
                    return None, "task list has invalid assignee"
                
                project_details["tasks"].append({
                    "id": task.id, 
                    "name": task.name, 
                    "description": task.description, 
                    "assignee": {
                        "id": assignee.id, 
                        "name": assignee.name, 
                        "email": assignee.email,
                    }, 
                    "status": task.status, 
                    "created_at": task.created_at, 
                })

            return project_details

    def get_members(self, project_id: str, user_id: str):
        members_list = []
        with self.session() as session:
            project_membership = session.query(Project, Membership).filter(and_(Project.id==Membership.project_id, Project.id==project_id, Membership.user_id==user_id)).first()
            if not project_membership:
                return None, "user is not part of the project"

            project_members = session.query(Project, Membership).filter(and_(Project.id==Membership.project_id, Project.id==project_id)).all()
            for row in project_members:
                member = row[1]
                user = session.query(User).filter(User.id==member.user_id).first()
                if not user:
                    return None, "unknown member found"
                
                members_list.append({
                    "id": user.id, 
                    "name": user.name, 
                    "email": user.email, 
                    "role": member.role.value
                })
            
            return members_list, None

    def delete_project(self, project_id: str, user_id: str):
        with self.session() as session:
            project = session.get(Project, project_id)
            if not project:
                return "project does not exist"
            
            project_membership = session.query(Project, Membership).filter(and_(Project.id==Membership.project_id, Project.id==project_id, Membership.user_id==user_id)).first()
            if not project_membership:
                return "user is not part of the project"

            if project_membership[1].role != Role.Owner:
                return "user is not the project owner"
            
            session.delete(project)
            session.commit()

    def join_project(self, project_code: str, user_id: str):
        with self.session() as session:
            project = session.query(Project).filter(Project.code==project_code).first()
            if not project:
                return "project code invalid"
            
            project_membership = session.query(Project, Membership).filter(and_(Project.id==Membership.project_id, Project.id==project.id, Membership.user_id==user_id)).first()
            if project_membership:
                return "user already a member of this project"
            
            member = Membership(user_id=user_id, project_id=project.id, role=Role.Member)
            session.add(member)
            session.commit()

    def create_task(self, name: str, description: str, assignee: str, status: TaskStatus, project_id: str):
        pass