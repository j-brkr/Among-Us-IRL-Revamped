
$( document ).ready(function(){
    updatePage();
    setInterval(updatePage, 1000);
});

function updatePage(){
    $.get( "/api/game", function(game){
        console.log(game);
        loadPage(game["status"]);

    })
    .fail(function(){
        console.log("GET Failed")
        document.write("GET Failed. Maybe there is no active game")
    });
}

const lobby_page = {
    selector: "#lobby",
    backgroundColor: "black",
    update: updateLobby
}

function updateLobby(status){
    $.get("/api/game/players", function(players){
        console.log(players);
        // Player List
        $( "#playerList" ).empty();
        players.forEach(function(player){
            let playerDisplay = $( '<div class="player"></div>' )
                .text(player["user"]["name"])
                .css("background-color", player["user"]["color"] + "A0");
            $( "#playerList" ).append(playerDisplay)
        })
        // Start Game Button
        $( '#startGame' ).text("Start Game ("+players.length+" "+(players.length==1?"player":"players")+")").prop("disabled", players.length < 5);
    })
}

const reveal_page = {
    selector: "#role-reveal",
    backgroundColor: "black"
}

const game_page = {
    selector: "#game",
    backgroundColor: "blue"
}

const meeting_page = {
    selector: "#voting",
    backgroundColor: "blue"
}

const pages={
    "LOBBY": lobby_page,
    "GAME": game_page,
    "MEETING": meeting_page
}

function loadPage(status){
    $( ".page" ).css("display", "none");
    let page = pages[status];
    $( page.selector ).css("display", "block");
    $( "body" ).css("background-color", page.backgroundColor);
    page.update();
}

function startGame(){
    $.post("/central", "START_GAME", function(){
        alert("The game is starting");
    })
}



