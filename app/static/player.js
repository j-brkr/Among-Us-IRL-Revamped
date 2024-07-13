$( document ).ready(function(){
    $.get( "/api/game", function(game){
        console.log(game);
        loadPage(game["status"]);

    })
    .fail(function(){
        console.log("GET Failed")
        document.write("GET Failed. Maybe there is no active game")
    });
})

const lobby_page = {
    title: "Lobby",
    selector: "#lobby"
}

const role_reveal_page = {
    title: "Role Reveal",
    selector: "#role-reveal"
}

const game_page = {
    title: "Game",
    selector: "#game"
}

const meeting_page = {
    title: "Meeting",
    selector: "#meeting"
}

const pages={
    "LOBBY": lobby_page,
    "GAME": game_page,
    "MEETING": meeting_page
}

function loadPage(status){
    $( ".page" ).css("display", "none");
    let page = pages[status];
    $( 'title' ).text("Among Us IRL - " + page.title)
    $( page.selector ).css("display", "block");
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
            console.log("Success: " + result)
        }
    });
}