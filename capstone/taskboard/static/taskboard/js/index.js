// open the taskboard modal
function openTaskboardModal() {
    console.log("openTaskboardModal........... start");
    var taskboardModal = document.getElementById('taskboardModal');
    taskboardModal.style.display = "inline-block"; 
}

// close the taskboard modal
function closeTaskboardModal() {
    console.log("closeTaskboardModal........... start");
    var taskboardModal = document.getElementById('taskboardModal');
    console.log(document.getElementById('taskboard_name').value);
    taskboardModal.style.display="none";
}

// reset create taskboard modal form
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
    load_all_users(null);
}

// Setting up the create taskboard modal
function createTaskboard() {
    document.getElementById('taskboard-modal-title').innerHTML = "Create Taskboard";
    document.getElementById('taskboard_form').action = "/taskboard/create";
    document.getElementById('submit-taskboard-btn').innerHTML = "Create";

    resetForm();
    openTaskboardModal();
}

// Fetching api to loading users for the datalist dropdown
function load_all_users(listToExcludeAsStr) {
    var listToExclude = convertStrToListOfNumbers(listToExcludeAsStr);
    console.log("listToExclude:");
    console.log(listToExclude); 
    console.log(document.getElementById('members').innerHTML.length)
    if (document.getElementById('members').innerHTML.length > 0) {
        document.getElementById('members').innerHTML = "";
    }
    fetch(`/taskboards/load_users`)
    .then(response => response.json())
    .then(data => {
        all_users = data["all_users"]
        console.log(all_users)

        for (index in all_users) {
            user = all_users[index];
            if (listToExclude && listToExclude.includes(user["id"])) {
                console.log("continue")
                continue;
            } else {
                console.log("include")
                const member_option = document.createElement('option');
                member_option.value = user["username"];
                member_option.dataset.value = user["id"];
                document.getElementById('members').append(member_option);
            }
        }
    })
}

// Helper Function: Conver "ID,ID,ID" INTO [ID,ID,ID] (Arr Type = Number)
function convertStrToListOfNumbers(str) {
    var arrOfStr = null;
    var arrOfNum = null;
    if (str) {
        arrOfStr = str.split(",");
    }
    if (arrOfStr) {
        arrOfNum = [];
        arrOfStr.forEach(s => {
            arrOfNum.push(Number(str));
        });
    }
    return arrOfNum;
}

// Show the Add Members view on modal form
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

// Adding member to form[taskboard_members]
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
            <div class="chip" id='member-${member_to_be_added}'>
                ${shownVal}
                <span class="closebtn" onclick="removeMember('${member_to_be_added}');">&times;</span>
            </div>
        `;
        // displaying newly added member
        document.getElementById('showMemberList').append(x);

        // resetting member_to_be_added field
        document.getElementById('member_to_be_added').value = "";

        // reload members list
        let currentMembersListStr = document.getElementById('taskboard_members').value;
        load_all_users(currentMembersListStr);
    }
}

// remove member from form[taskboard_members]
function removeMember(id) {
    let currentMembersListStr = document.getElementById('taskboard_members').value;
    var newList = convertStrToListOfNumbers(currentMembersListStr);
    console.log("newList before splice: " + newList.toString());
    // removing id from members list
    for( var i = 0; i < newList.length; i++){                       
        if ( newList[i] == id) { 
            newList.splice(i, 1); 
            break;
        }
    }
    console.log("newList after splice: " + newList.toString());
    // updating members list
    document.getElementById('taskboard_members').value = newList.toString();
    
    // remove member from show member list
    document.getElementById(`member-${id}`).remove();
    console.log("taskboard_members");
    console.log(document.getElementById('taskboard_members').value);
    // load users for dropdown again
    load_all_users(newList.toString());
}