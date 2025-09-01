from datetime import datetime
from sqlalchemy import and_

from db import Database
from utils.id import generate_id
from models import Project, User, Membership
from models.membership import Role

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
                    "role": member.role, 
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

            with session.begin():
                session.add(project_instance)
                session.add(member)

            return {
                "id": project_instance.id, 
                "name": project_instance.name, 
                "description": project_instance.description, 
                "deadline": project_instance.deadline, 
                "code": project_instance.code, 
                "created_at": project_instance.created_at.strftime("%Y-%m-%d %I:%M:%S %p")
            }

    def get_project(self, project_id: str):
        pass