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