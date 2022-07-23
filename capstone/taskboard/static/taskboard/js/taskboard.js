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

function resetTaskForm() {
    document.getElementById('task_name').value = "";
    document.getElementById('task_description').value = "";
    document.getElementById('task_deadline').value = "";
}

function openTaskModal(boardId) {
    document.getElementById('taskModal').style.display = "block";
    var getTaskboardUrl = `/taskboard/${boardId}/view`;
    fetch(getTaskboardUrl)
    .then(response => response.json())
    .then(data => {
        document.getElementById('task_assignee').innerHTML = "";
        taskboard_owner = data["taskboard_owner"]["username"];
        const member_option = document.createElement('option');
        member_option.value = taskboard_owner;
        member_option.innerHTML = taskboard_owner;
        document.getElementById('task_assignee').append(member_option);

        taskboard_members = data["taskboard_members"];
        for (member in taskboard_members) {
            const member_option = document.createElement('option');
            member_option.value = taskboard_members[member]["username"];
            member_option.innerHTML = taskboard_members[member]["username"];
            document.getElementById('task_assignee').append(member_option);
        }
    })
}

function closeTaskModal() {
    document.getElementById('taskModal').style.display = "none";
}

