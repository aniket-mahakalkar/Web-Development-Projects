// console.log('Hello, world!');

// get elements

let taskInput = document.getElementById('task-input');
let taskList = document.getElementById('task-list');
let addTaskButton = document.getElementById('add-task-btn');


// add event listeners
let tasks = JSON.parse(localStorage.getItem('tasks')) || [];


// function formatDate(date) {

//     let now = new Date(date);
//     let taskDate = now.Date(date);
//     let diffInMilliSeconds = (now - taskDate);
//     let diffInSeconds = diffInMilliSeconds / 1000;
//     let diffInMinutes = diffInSeconds / 60;
//     let diffInHours = diffInMinutes / 60;
//     let diffInDays = diffInHours / 24;
//     let diffInMonths = diffInDays / 30;
//     let diffInYears = diffInDays / 365;

//     let timeAgo = "";

//     if (diffInDays < 1) {
//         timeAgo = 'Just Now';
//     } else if (diffInDays < 2) {
//     }
// Toggle Task
function toggleTask(index) {
    tasks[index].completed = !tasks[index].completed;
    localStorage.setItem('tasks', JSON.stringify(tasks));
    displayTasks();
}



// delete task

function deleteTask(index){

    tasks.splice(index,1);
    localStorage.setItem('tasks',JSON.stringify(tasks));
    displayTasks();
}

//Display tasks
function displayTasks() {
    
    taskList.innerHTML = '';
    tasks.forEach((task, index) => {
        let taskItem = document.createElement('li');
        
        if (task.completed) {

            taskItem.classList.add('completed');
        }


        taskItem.innerHTML = `
        <div class="task">
            <div class="task-text-n-date">
                <span class="task-text">${task.text}</span>
                <span class="task-date">${task.Date}</span>
            </div>
    
            <div class="task-actions">
                <button class="edit-btn" onclick = "editTask(${index})">Edit</button>
                <button class="delete-btn" onclick = "deleteTask(${index})">Delete</button>
                <button class="toggle-btn" onclick="toggleTask(${index})">${task.completed ? "Unmark":"Completed"}</button>
            </div>
        </div>
        `;

    
        taskList.appendChild(taskItem);
    });
}


// Add Task Button
addTaskButton.addEventListener("click",() => {
    let taskText = taskInput.value.trim();    
    if(taskText){
        
        let newTask ={
            text: taskText,
            Date: new Date().toISOString(),
            completed: false
        };

        tasks.push(newTask);
        localStorage.setItem('tasks', JSON.stringify(tasks));
        taskInput.value = '';
        displayTasks();
    }else{
        alert('Please enter a task');
    }

    
});


function editTask(index){
    let taskText = prompt('Edit Task', tasks[index].text);
    if(taskText){
        tasks[index].text = taskText;
        localStorage.setItem('tasks', JSON.stringify(tasks));
        displayTasks();
    }
}

displayTasks();