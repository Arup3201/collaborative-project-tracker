# Collaborative Project Tracker

## Setup

### Backend

Follow these steps to setup the backend:

#### Step 1: Create virtual environment

```sh
cd backend
python -m venv .venv
```

#### Step 2: Activate virtual environment

```sh
.\.venv\Scripts\activate # windows
```

#### Step 3: Install libraries

```sh
pip install -r requirements.txt
```

#### Step 4: Start the server

```sh
python app.py
```

This will start the server at `localhost:8000`

### Frontend

Follow these steps to setup frontend:

#### Step 1: Install dependencies

```sh
cd frontend
npm install
```

#### Step 2: Run the frontend

```sh
npm run dev
```

This should open the frontend at `localhost:5173`

### nginx for CORS

#### Step 1: Update nginx.conf file
`nginx.conf` file:

```conf

worker_processes  1;

events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;

        location / {
            proxy_pass http://localhost:5173;
        }

        location /api {
            proxy_pass http://localhost:8000;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```

#### Step 2: Run nginx

Windows:

```sh
cd nginx
start nginx
```

## Details

Collaborative project management web app where users can -

- add projects
- collaborate on projects
- add task in projects
- assign task to members
- join projects using project code
- track tasks for each project

and also restricts users based on their role in the project.

Owners of a project has permission to -

- delete the project
- create task
- assign task to a member
- change task status

Members of a project has permission to -

- see the project
- see the tasks
- change the task status he is part of

## Tech Stack

### Backend

- Language: Python
- Web Framwork: Flask
- ORM: SQLAlchemy
- Validatoin: Pydantic
- Database: PostgreSQL

I have chooses **Python** for building this project because it helps me make the prototypes faster and it is really good for rapid development. In Python, for web dev I am using **Flask** because of it's lightweight nature, easy syntax for building the APIs and middlewares. As the database, I have chosen **PostgreSQL** because of it's reliable nature, ability to solve complex queries. Also it gives great performance and helps me scale this project. I am using **Pylance** for early bug fixing in my IDE, **Pydantic** will validate the incoming requests and let the user know the correct input structure. **SQLAlchemy** helps me communitate and manage the database connections gracefully, while it also removes the complexity the writing the queries from scratch.

### Frontend

- Language: Typescript
- Framework: ReactJS

## Database models

### User Table

**Usage**: Stores user account information for authentication and identification throughout the application.

**Columns**:
- `id` (String, 150 chars) - Unique identifier for each user, primary key
- `name` (String, 50 chars) - User's display name, required
- `email` (String, 150 chars) - User's email address for login, required
- `password_hash` (String, 150 chars) - Hashed password for security, required
- `created_at` (DateTime) - Account creation timestamp, auto-generated

### Project Table

**Usage**: Stores project information including details, deadlines, and unique join codes for collaboration.

**Columns**:
- `id` (String, 150 chars) - Unique identifier for each project, primary key
- `name` (String, 150 chars) - Project title/name, required
- `description` (String) - Detailed project description, optional
- `deadline` (DateTime) - Project completion deadline, required
- `created_at` (DateTime) - Project creation timestamp, auto-generated
- `code` (String) - Unique join code for users to join the project, required

### Task Table

**Usage**: Stores individual tasks within projects, tracking assignment, status, and progress.

**Columns**:
- `id` (String, 150 chars) - Unique identifier for each task, primary key
- `name` (String, 150 chars) - Task title/name, required
- `description` (String) - Detailed task description, optional
- `created_at` (DateTime) - Task creation timestamp, auto-generated
- `assignee` (String) - Foreign key to users.id, identifies task assignee
- `status` (Enum: TaskStatus) - Current task status (To Do, In Progress, Completed)
- `project_id` (String) - Foreign key to projects.id, links task to project

### Membership Table

**Usage**: Junction table managing many-to-many relationships between users and projects with role-based access control.

**Columns**:
- `user_id` (String) - Foreign key to users.id, part of composite primary key
- `project_id` (String) - Foreign key to projects.id, part of composite primary key
- `role` (Enum: Role) - User's role in the project (Member, Owner)
- `created_at` (DateTime) - Membership creation timestamp, auto-generated

### Table Relationships

#### User ↔ Project (Many-to-Many via Membership)
- **Users** can be members of multiple **Projects**
- **Projects** can have multiple **Users** as members
- Relationship managed through **Membership** table with role-based permissions

#### User → Task (One-to-Many)
- **Users** can be assigned to multiple **Tasks**
- Each **Task** has exactly one **User** as assignee

#### Project → Task (One-to-Many)
- **Projects** contain multiple **Tasks**
- Each **Task** belongs to exactly one **Project**

#### User → Membership (One-to-Many)
- **Users** can have multiple **Memberships** (different projects)
- Each **Membership** belongs to exactly one **User**

#### Project → Membership (One-to-Many)
- **Projects** can have multiple **Memberships** (different users)
- Each **Membership** belongs to exactly one **Project**

## API endpoints

### Authentication endpoints

#### Register user

**Usage**: Create a new user account with email and password authentication

**Rule**: `/api/v1/auth/register`

**Method**: `POST`

**Payload**: 
```json
{
  "username": "string",
  "email": "string", 
  "password": "string"
}
```

**Response**:
```json
{
  "message": "User registered successfully",
  "user_id": "string"
}
```

**Response Code**: 201

**Errors**:
- `400` - Invalid inputs (email, name, password)
- `409` - email already exists
- `422` - Validation errors
- `500` - Server error (code logic problem)

#### Login User

**Usage**: Authenticate user and obtain access token for protected endpoints

**Rule**: `/login`

**Method**: `POST`

**Payload**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Response Body**:

```json
{
  "user": {
    "id": "string",
    "name": "string",
    "email": "string"
  }
}
```

**Response Cookie**: 

JWT token payload

```json
{
    "user": {
        "id": "string",
        "name": "string",
        "email": "string"
    }
}
```

**Errors**:
- `400` - Missing email or password
- `422` - Validation error
- `500` - Server error (code logic problem)

### Project Endpoints

#### List Projects

**Usage**: Get all projects that the authenticated user is a member of

**Rule**: `/api/v1/projects/`

**Method**: `GET`

**Payload**: None (requires authentication header)

**Response**:
```json
{
  "projects": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "deadline": "datetime",
      "code": "string",
      "role": "Member|Owner", 
      "created_at": "str(format: 2025-09-02 09:20 PM)"
    }
  ]
}
```

**Errors**:
- `401` - Unauthorized (invalid or missing token)
- `500` - Server error (code logic problem)

#### Create Project

**Usage**: Create a new project with the authenticated user as owner

**Rule**: `/api/v1/projects/`

**Method**: `POST`

**Payload**:
```json
{
  "name": "string",
  "description": "string (optional, defaults to empty)",
  "deadline": "datetime"
}
```

**Response**:
```json
{
  "message": "Project created successfully",
  "project": {
    "id": "string",
    "name": "string",
    "description": "string",
    "deadline": "datetime",
    "code": "string",
    "created_at": "str(format: 2025-09-02 09:20 PM)"
  }
}
```

**Response Code**: 201

**Errors**:
- `400` - Invalid input data
- `401` - Unauthorized
- `404` - Invalid user
- `422` - Validation errors
- `500` - Server error (code logic error)

#### Get Project Details

**Usage**: Retrieve detailed information about a specific project including all tasks

**Rule**: `/api/v1/projects/<project_id>`

**Method**: `GET`

**Payload**: None (requires authentication header)

**Response**:
```json
{
  "project": {
    "id": "string",
    "name": "string",
    "description": "string",
    "deadline": "datetime",
    "code": "string",
    "created_at": "str(format: 2025-09-02 09:20 PM)"
  },
  "tasks": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "assignee": "string",
      "assignee_name": "string",
      "assignee_email": "string",
      "status": "To Do|In Progress|Completed",
      "created_at": "str(format: 2025-09-02 09:20 PM)"
    }, 
    // ...
  ]
}
```

**Errors**:
- `404` - Project not found
- `403` - User not a member of the project
- `401` - Unauthorized
- `500` - Server error (code logic error)

#### Delete Project

**Usage**: Permanently delete a project (only accessible to project owners)

**Rule**: `/api/v1/projects/<project_id>`

**Method**: `DELETE`

**Payload**: None (requires authentication header)

**Response**:
```json
{
  "message": "Project deleted successfully"
}
```

**Errors**:
- `404` - Project not found
- `403` - User not the project owner
- `401` - Unauthorized
- `500` - Server error (code logic error)

#### Get Project Members

**Usage**: Retrieve list of all members in a specific project with their roles

**Rule**: `/api/v1/projects/<project_id>/members`

**Method**: `GET`

**Payload**: None (requires authentication header)

**Response**:
```json
{
  "members": [
    {
      "user_id": "string",
      "name": "string",
      "email": "string",
      "role": "Member|Owner",
      "joined_at": "str(format: 2025-09-02 09:20 PM)"
    }, 
    // ...
  ]
}
```

**Errors**:
- `404` - Project not found
- `403` - User not a member of the project
- `401` - Unauthorized
- `500` - Server error (code logic error)

#### Join Project by Code

**Usage**: Join an existing project using its unique join code

**Rule**: `/api/v1/projects/join/code/<project_code>`

**Method**: `POST`

**Payload**: None (requires authentication header)

**Response**:
```json
{
  "message": "Successfully joined project",
  "project": {
    "id": "string",
    "name": "string",
    "description": "string"
  }
}
```

**Errors**:
- `404` - Invalid project code
- `409` - User already a member of the project
- `401` - Unauthorized
- `500` - Server error (code logic error)

### Task Endpoints

#### Create Task

**Usage**: Create a new task within a specific project

**Rule**: `/api/v1/projects/<project_id>/tasks/`

**Method**: `POST`

**Payload**:
```json
{
  "name": "string",
  "description": "string (optional, defaults to empty)",
  "assignee": "string",
  "status": "To Do|In Progress|Completed"
}
```

**Response**:
```json
{
  "message": "Task created successfully",
  "task": {
    "id": "string",
    "name": "string",
    "description": "string",
    "assignee": "string",
    "status": "To Do",
    "created_at": "str(format: 2025-09-02 09:20 PM)"
  }
}
```

**Errors**:
- `404` - Project not found
- `403` - User not a member of the project
- `400` - Invalid name/assignee/status (not a project member)
- `422` - Validation errors
- `401` - Unauthorized
- `500` - Server error (code logic error)

#### Get Task Details

**Usage**: Retrieve detailed information about a specific task

**Rule**: `/api/v1/projects/<project_id>/tasks/<task_id>`

**Method**: `GET`

**Payload**: None (requires authentication header)

**Response**:
```json
{
  "task": {
    "id": "string",
    "name": "string",
    "description": "string",
    "assignee": "string",
    "assignee_name": "string",
    "status": "To Do|In Progress|Completed",
    "created_at": "str(format: 2025-09-02 09:20 PM)",
    "project_id": "string"
  }
}
```

**Errors**:
- `404` - Task or project not found
- `403` - User not a member of the project
- `401` - Unauthorized
- `500` - Server error (code logic error)

#### Edit Task

**Usage**: Update task details such as name, description, and assignee

**Rule**: `/api/v1/projects/<project_id>/tasks/<task_id>`

**Method**: `PUT`

**Payload**:
```json
{
  "name": "string (optional, defaults to empty)",
  "description": "string (optional, defaults to empty)"
}
```

**Response**:
```json
{
  "message": "Task updated successfully",
  "task": {
    "id": "string",
    "name": "string",
    "description": "string",
    "assignee": "string",
    "assignee_name": "string",
    "assignee_email": "string",
    "status": "string",
    "created_at": "str(format: 2025-09-02 09:20 PM)"
  }
}
```

**Errors**:
- `404` - Task or project not found
- `403` - User not a member of the project
- `400` - Invalid assignee (not a project member)
- `422` - Validation errors
- `401` - Unauthorized
- `500` - Server error (code logic error)

#### Change Task Status

**Usage**: Update the status of a task (To Do, In Progress, Completed)

**Rule**: `/api/v1/projects/<project_id>/tasks/<task_id>/status`

**Method**: `PUT`

**Payload**:
```json
{
  "status": "To Do|In Progress|Completed"
}
```

**Response**:
```json
{
  "message": "Task status updated successfully",
  "task": {
    "id": "string",
    "status": "string"
  }
}
```

**Errors**:
- `404` - Task or project not found
- `403` - User not a member of the project
- `400` - Invalid status value
- `401` - Unauthorized
- `500` - Server error (code logic error)

#### Change Task Assignee

**Usage**: Reassign a task to a different project member

**Rule**: `/api/v1/projects/<project_id>/tasks/<task_id>/assign`

**Method**: `PUT`

**Payload**:
```json
{
  "assignee": "string"
}
```

**Response**:
```json
{
  "message": "Task assignee updated successfully",
  "task": {
    "id": "string",
    "assignee": "string",
    "assignee_name": "string"
  }
}
```

**Errors**:
- `404` - Task or project not found
- `403` - User not a member of the project
- `400` - Invalid assignee (not a project member)
- `401` - Unauthorized
- `500` - Server error (code logic error)