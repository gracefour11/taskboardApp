function openTaskboardModal() {
    console.log("openTaskboardModal........... start");
    var taskboardModal = document.getElementById('taskboardModal');
    taskboardModal.style.display = "inline-block"; 
    // loadMembersList();
}

function closeTaskboardModal() {
    console.log("closeTaskboardModal........... start");
    var taskboardModal = document.getElementById('taskboardModal');
    console.log(document.getElementById('taskboard_name').value);
    taskboardModal.style.display="none";
}

function resetForm() {
    document.getElementById('taskboard_name').value = "";
    document.getElementById('taskboard_deadline').value = "";
    var ele = document.querySelectorAll('input[name = "taskboard_type"]');
    for(var i=0;i<ele.length;i++)
       ele[i].checked = false;
       console.log(ele);
    document.getElementById('taskboard_members').value = "";
    document.getElementById('showMemberList').innerHTML = "";
    document.getElementById('showAddMembersDiv').style.display = "none";
}

function createTaskboard() {
    document.getElementById('taskboard-modal-title').innerHTML = "Create Taskboard";
    document.getElementById('taskboard_form').action = "/taskboard/create";
    document.getElementById('submit-taskboard-btn').innerHTML = "Create";

    resetForm();
    openTaskboardModal();
}

function showAddMembersView() {
    console.log("in showAddMembersView()");
    var selected_type = document.querySelector('input[name = "taskboard_type"]:checked').value;
    console.log("selected_type: " + selected_type);
    if (selected_type == 'GRP') {
        document.getElementById('showAddMembersDiv').style.display = "block";
    } else {
        document.getElementById('showAddMembersDiv').style.display = "none";
    }
}

function addMember() {
    var shownVal = document.getElementById('member_to_be_added').value;
    var member_to_be_added = document.querySelector("#members option[value='"+shownVal+"']").dataset.value;

    if (member_to_be_added != "") {
        // console.log(member_to_be_added);
        var addedMemberListInForm = document.getElementById('taskboard_members').value;
        if (addedMemberListInForm == "") {
            addedMemberListInForm = member_to_be_added
        } else {
            addedMemberListInForm += "," + member_to_be_added;
        }
        document.getElementById('taskboard_members').value = addedMemberListInForm;
        var x = document.createElement("div");
        x.innerHTML = `
            <p>${shownVal}</p>
        `;
        // displaying newly added member
        document.getElementById('showMemberList').append(x);

        // resetting member_to_be_added field
        document.getElementById('member_to_be_added').value = "";
    }
}
