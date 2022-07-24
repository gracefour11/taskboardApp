function resetSectionForm() {
    document.getElementById('section_name').value = "";
}

function openSectionModal() {
    document.getElementById('sectionModal').style.display = "block";
}

function closeSectionModal() {
    document.getElementById('sectionModal').style.display = "none";
}

// Setting up the create section modal
function createSection(boardId) {
    document.getElementById('section-modal-title').innerHTML = "Create Section";
    document.getElementById('section_form').action = `/taskboard/${boardId}/section/create`;
    document.getElementById('submit-section-btn').innerHTML = "Create";

    resetSectionForm();
    openSectionModal();
}

// Setting up the edit section modal
function editSection(boardId, sectionId, sectionName) {
    document.getElementById('section-modal-title').innerHTML = "Rename Section";
    document.getElementById('section_form').action = `/taskboard/${boardId}/section/${sectionId}/edit`;
    document.getElementById('submit-section-btn').innerHTML = "Save Changes";
    document.getElementById('section_name').value = sectionName;
    openSectionModal();
}

function openDeleteSectionModal(boardId, sectionId) {
    document.getElementById('deleteSectionModal').style.display = "block";
    document.getElementById('delete_section_form').action =  `/taskboard/${boardId}/section/${sectionId}/delete`;
}

function closeDeleteSectionModal() {
    document.getElementById('deleteSectionModal').style.display = "none";
}

// Setting up the create task modal
function createTask(boardId, sectionId) {
    document.getElementById('task-modal-title').innerHTML = "Create Task";
    document.getElementById('task_form').action = `/taskboard/${boardId}/section/${sectionId}/task/create`;
    document.getElementById('submit-task-btn').innerHTML = "Create";
    resetTaskForm();
    openTaskModal(boardId);
}

function editTask(boardId, sectionId, taskId) {
    resetTaskForm();

    var getTaskUrl = `/taskboard/${boardId}/section/${sectionId}/task/${taskId}`;
    var editTaskUrl = `/taskboard/${boardId}/section/${sectionId}/task/${taskId}/edit`;

    document.getElementById('task-modal-title').innerHTML = "Edit Task";
    document.getElementById('task_form').action = editTaskUrl;
    document.getElementById('submit-task-btn').innerHTML = "Save Changes";
    
    openTaskModal(boardId);

    fetch(getTaskUrl)
    .then(response => response.json())
    .then(task => {
        console.log(task);
        document.getElementById('task_name').value = task.name;
        document.getElementById('task_deadline').value = task.deadline;
        document.getElementById('task_description').value = task.description;
        document.getElementById('task_assignee').value = task.assignee;
        console.log(document.getElementById('task_assignee').value);
    });
}

function confirmDelete(boardId, sectionId, taskId) {
    var result = confirm("Are you sure you want to delete this task?");
    if (result) {
        deleteTask(boardId, sectionId, taskId);
    }
}

function deleteTask(boardId, sectionId, taskId) {
    fetch(`/taskboard/${boardId}/section/${sectionId}/task/${taskId}/delete`, {
        method: 'POST',
        body: JSON.stringify({
            delete_ind: 'T'
        })
    })
    .then(response => response.json())
    .then(() => {
        document.location.reload();
    });
}

function resetTaskForm() {
    document.getElementById('task_name').value = "";
    document.getElementById('task_description').value = "";
    document.getElementById('task_deadline').value = "";
}

function openTaskModal(boardId) {
    document.getElementById('taskModal').style.display = "block";
}

function closeTaskModal() {
    document.getElementById('taskModal').style.display = "none";
}



