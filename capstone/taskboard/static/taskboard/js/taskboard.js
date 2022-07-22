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
