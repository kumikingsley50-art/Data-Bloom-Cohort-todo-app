from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

class TodoCreate(BaseModel):
    title: str
    description: str

def get_connection():
    connection = sqlite3.connect("todos.db")
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    connection.commit()
    connection.close()

initialize_database()

@app.get("/")
def home():
    return {"message": "Todo API is running"}

@app.get("/todos", response_model=list[Todo])
def get_todos():
    connection = get_connection()
    cursor = connection.execute("SELECT * FROM todos")
    rows = cursor.fetchall()
    connection.close()

    todos_list = [Todo(**dict(row)) for row in rows]
    return todos_list

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    connection = get_connection()
    cursor = connection.execute(
        """
        INSERT INTO todos (title, description, completed)
        VALUES (?, ?, ?)
        """,
        (todo.title, todo.description, 0),
    )
    todo_id = cursor.lastrowid
    connection.commit()
    connection.close()
    
    return Todo(id=todo_id, title=todo.title, description=todo.description, completed=False)

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, completed: bool):
    connection = get_connection()
    
    # Check if exists
    cursor = connection.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    if cursor.fetchone() is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Todo not found")
        
    connection.execute(
        """
        UPDATE todos
        SET completed = ?
        WHERE id = ?
        """,
        (int(completed), todo_id),
    )
    connection.commit()
    connection.close()
    return {"message": "Todo updated"}
