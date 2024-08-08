// Function to get the JWT token from local storage
function getAuthToken() {
    return localStorage.getItem('access');
}



// Function to load tasks
function loadTasks() {
    axios.get('/tasks/', {
        headers: {
            'Authorization': 'Bearer ' + getAuthToken()
        }
    })
        .then(response => {
            const tasksTableBody = document.getElementById('tasks-table-body');
            const taskCounter = document.getElementById('task-counter');
            const tasksMessage = document.getElementById('tasks-message');
            tasksTableBody.innerHTML = '';
            const tasks = response.data;
            taskCounter.textContent = `Total Tasks: ${tasks.length}`;

            if (tasks.length === 0) {
                tasksMessage.textContent = "No tasks for you. Please add one.";
            } else {
                response.data.forEach(task => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${task.title}</td><td>${task.due_date}</td><td>${task.category}</td><td><button onclick="deleteTask(${task.id})">Delete</button></td>`;
                    tasksTableBody.appendChild(row);
                });
            }
        })
        .catch(error => {
            if (error.response && error.response.status === 401) {
                // Redirect to login page if unauthorized
                window.location.href = '/login/';
            }
        });
}


// Function to delete a task
function deleteTask(taskId) {
    axios.delete(`/tasks/${taskId}/delete/`, {
        headers: {
            'Authorization': 'Bearer ' + getAuthToken()
        }
    })
        .then(response => {
            console.log('Task deleted successfully');
            // Refresh the task list
            loadTasks();
        })
        .catch(error => {
            if (error.response && error.response.status === 401) {
                // Redirect to login page if unauthorized
                window.location.href = '/login/';
            }
        });
}

// Function to search tasks by title
function searchTasks(title) {
    axios.get('/tasks/search/', {
        params: { title: title },
        headers: {
            'Authorization': 'Bearer ' + getAuthToken()
        }
    })
        .then(response => {
            const tasksTableBody = document.getElementById('tasks-table-body');
            const taskCounter = document.getElementById('task-counter');
            tasksTableBody.innerHTML = '';
            const tasks = response.data;
            taskCounter.textContent = `Total Tasks: ${tasks.length}`;
            const tasksMessage = document.getElementById('tasks-message');
            if (tasks.length === 0) {
                tasksMessage.textContent = "No tasks for you. Please add one.";
            } else {
                response.data.forEach(task => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${task.title}</td><td>${task.due_date}</td><td>${task.category}</td><td><button onclick="deleteTask(${task.id})">Delete</button></td>`;
                    tasksTableBody.appendChild(row);
                });
            }
        })
        .catch(error => {
            if (error.response && error.response.status === 401) {
                // Redirect to login page if unauthorized
                window.location.href = '/login/';
            }
        });
}

// Attach event listeners
document.getElementById('task-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const title = document.getElementById('title').value;
    const due_date = document.getElementById('due_date').value;
    const category = document.getElementById('category').value;
    addTask(title, due_date, category);
});

document.getElementById('load-tasks').addEventListener('click', function () {
    loadTasks();
});

document.getElementById('search-button').addEventListener('click', function () {
    const title = document.getElementById('search-title').value;
    searchTasks(title);
});

// Initial load of tasks
loadTasks();
