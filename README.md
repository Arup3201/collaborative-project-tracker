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