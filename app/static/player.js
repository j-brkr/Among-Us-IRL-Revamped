let page = "NONE"

$( document ).ready(function(){
    checkStatus();
    setInterval(checkStatus, 2000);
})

function checkStatus(){
    $.get( "/api/game", function(game){
        console.log(game);
        if(game["status"] != page.status){
            //console.log("Status mismatch: " + game["status"] + " and " + page.status)
            loadPage(game["status"]);
        }
    })
    .fail(function(){
        console.log("GET Failed")
        document.write("Connection Lost!")
    });
}

const lobby_page = {
    status: "LOBBY",
    title: "Lobby",
    selector: "#lobby"
}

const role_reveal_page = {
    status: "REVEAL",
    title: "Role Reveal",
    selector: "#role-reveal"
}

const game_page = {
    status: "GAME",
    title: "Game",
    selector: "#game",
    load: function(){
        this.update();
    },
    update: function(){
        //$( "#taskBox" ).empty();
        $.get("/player-task_box", function(data){
            $( "#taskBox" ).html(data);
        });
    }
}

const meeting_page = {
    status: "MEETING",
    title: "Meeting",
    selector: "#meeting",
    load: function(){
        audio = $( "#emergencyAudio" )[0];
        audio.play();
    }
}

const pages={
    "LOBBY": lobby_page,
    "GAME": game_page,
    "MEETING": meeting_page
}

function loadPage(status){
    $( ".page" ).css("display", "none");
    page = pages[status];
    $( 'title' ).text("Among Us IRL - " + page.title)
    $( page.selector ).css("display", "block");
    if("load" in page) page.load();
}

function taskClick(playerTaskId, completed){
    let put_data = JSON.stringify({"completed": completed});
    console.log(put_data);
    $.ajax({
        url: "/api/player_task/" + playerTaskId,
        type: 'PUT',
        data: put_data,
        contentType: "application/json",
        success: function (result){
            game_page.update();
        }
    });
}

function report(){
    $.post("command/EMERGENCY", function(data){
        checkStatus();
    });
}