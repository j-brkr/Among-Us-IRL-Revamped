
$( document ).ready(function(){
    $.get( "/api/game", function(game){
        console.log(game);
        changePage(game["status"]);

    })
    .fail(function(){
        console.log("GET Failed")
        document.write("GET Failed. Maybe there is no active game")
    });
})

function changePage(status){
    $( ".page" ).css("display", "none");
    switch(status) {
        case "LOBBY":
            $( "#lobby" ).css("display", "block");
            $( "body" ).css("background-color", "black");
            updateLobby();
            break;
        case "GAME":
            $( "#emergencyButton" ).css("display", "block");
            $( "body" ).css("background-color", "blue");
            break;
        case "VOTING":
            $( "#voting" ).css("display", "block");
            $( "body" ).css("background-color", "blue");
            break;
        default:
            console.log("Status " + status + " not recognized");
            break;
    }
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
        $( '#startGame' ).prop("disabled", players.length < 6);
    })
}

