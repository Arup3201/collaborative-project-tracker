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

### Step 2: Run the frontend

```sh
npm run dev
```

This should open the frontend at `localhost:5173`

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

### User ↔ Project (Many-to-Many via Membership)
- **Users** can be members of multiple **Projects**
- **Projects** can have multiple **Users** as members
- Relationship managed through **Membership** table with role-based permissions

### User → Task (One-to-Many)
- **Users** can be assigned to multiple **Tasks**
- Each **Task** has exactly one **User** as assignee

### Project → Task (One-to-Many)
- **Projects** contain multiple **Tasks**
- Each **Task** belongs to exactly one **Project**

### User → Membership (One-to-Many)
- **Users** can have multiple **Memberships** (different projects)
- Each **Membership** belongs to exactly one **User**

### Project → Membership (One-to-Many)
- **Projects** can have multiple **Memberships** (different users)
- Each **Membership** belongs to exactly one **Project**
