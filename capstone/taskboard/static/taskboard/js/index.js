function openTaskboardModal() {
    console.log("openTaskboardModal........... start");
    var taskboardModal = document.getElementById('taskboardModal');
    taskboardModal.style.display = "inline-block"; 
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
    load_all_users(null);
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
            <p id='member-${shownVal}'>${shownVal}</p>
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

function load_all_users(listToExcludeAsStr) {
    var listToExclude = convertStrToListOfNumbers(listToExcludeAsStr);
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
            console.log(user["id"]);
            console.log(typeof user["id"]);
            if (listToExclude != null && listToExclude.includes(user["id"])) {
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

function removeUserFromMembersList(listToExcludeAsStr, id) {
    var listToExclude = convertStrToListOfNumbers(listToExcludeAsStr);
    // removing id from members list
    for( var i = 0; i < listToExclude.length; i++){                       
        if ( listToExclude[i] === id) { 
            listToExclude.splice(i, 1); 
            break;
        }
    }
    // updating members list
    document.getElementById('taskboard_members').value = listToExclude.toString();
    
    // remove member from show member list
    document.getElementById(`member-${id}`).remove();

    // load users for dropdown again
    load_all_users(document.getElementById('taskboard_members').value);
}