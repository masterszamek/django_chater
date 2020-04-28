let loc = window.location;
let ws = new WebSocket("ws://"+loc.host+loc.pathname);

let data = new Object(); // general data


data.workspace_slug = loc.pathname.split('/')[2];
data.room_slug =  loc.pathname.split("/")[3];


let commands = {
    "set_user_status": function (status, username) {
        document.getElementById(username).className = "chatbox__user-list-status chatbox__user--"+status;

    },
    "get_users_status": function (users) {

        for (let key in users){
        document.getElementById(key).className = "chatbox__user-list-status chatbox__user--"+users[key];
        }
        console.log("get_users_status");
        console.log(users);

    },
    "username": function(username){
        data.username = username;
    },
    "new_message": function (who, text) {
        let html_code = `<div class="chatbox__messages__user-message--ind-message" style="float:right">` +
            `<p class="name"> ${who}</p>` +
            `<p class="message">${text}</p>` +
            `</div>`;
        document.getElementsByClassName("chatbox")[0].insertAdjacentHTML("beforeend", html_code);


    }
};


// return string
function to_JSON(ob){
    return JSON.stringify(ob);

}

// return JSON object
function decode_JSON(str){
    return JSON.parse(str);
}

ws.onmessage = function (event) {
    let msg = decode_JSON(event.data);
    console.log(msg)
    console.log(data.username)
    commands[msg.command](...msg.args)
};

$(document).ready(function () {

$("#cokolwiek").click(function (e) {
    console.log("www");
    e.stopPropagation();
})
});

/*
    {
        command: "asdadad"
        args: [ ]
    }

 */



