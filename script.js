const API_URL = "http://127.0.0.1:8000/todos";

const todoList = document.getElementById("todo-list");
const todoForm = document.getElementById("todo-form");
const titleInput = document.getElementById("title");
const descriptionInput = document.getElementById("description");

function fetchTodos() {
    fetch(API_URL)
        .then((response) => response.json())
        .then((todos) => {
            todoList.innerHTML = "";
            todos.forEach(todo => {
                const li = document.createElement("li");
                if (todo.completed) {
                    li.classList.add("completed");
                }

                const titleDiv = document.createElement("div");
                titleDiv.className = "todo-title";
                titleDiv.textContent = todo.title;

                const descDiv = document.createElement("div");
                descDiv.className = "todo-description";
                descDiv.textContent = todo.description;
                
                const actionsDiv = document.createElement("div");
                actionsDiv.className = "todo-actions";

                if (!todo.completed) {
                    const completeBtn = document.createElement("button");
                    completeBtn.className = "btn-complete";
                    completeBtn.textContent = "Complete";
                    completeBtn.addEventListener("click", () => {
                        completeTodo(todo.id);
                    });
                    actionsDiv.appendChild(completeBtn);
                }

                li.appendChild(titleDiv);
                li.appendChild(descDiv);
                li.appendChild(actionsDiv);

                todoList.appendChild(li);
            });
        });
}

function completeTodo(id) {
    fetch(`${API_URL}/${id}?completed=true`, {
        method: "PUT"
    })
    .then(() => fetchTodos());
}

todoForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const title = titleInput.value;
    const description = descriptionInput.value;

    fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title,
            description: description
        })
    })
        .then((response) => response.json())
        .then((createdTodo) => {
            titleInput.value = "";
            descriptionInput.value = "";
            fetchTodos();
        });
});

fetchTodos();
