let timeCounter = -1;

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
    update: function(){
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
}

const reveal_page = {
    selector: "#role-reveal",
    backgroundColor: "black",
    update: function(){
        timeCounter++;
        console.log("Reveal update" + timeCounter);
        if(timeCounter === 0){
            audio = $( "#revealAudio" )[0];
            console.log(audio)
            audio.play();
        }
        if(timeCounter === 5){
            // Reveal time is up
            $.post("/command/END_REVEAL", function(data){
                alert(data);
                updatePage();
            });
        }
    }
}

const game_page = {
    selector: "#game",
    backgroundColor: "#264775"
}

const meeting_page = {
    selector: "#voting",
    backgroundColor: "#264775"
}

const pages={
    "LOBBY": lobby_page,
    "GAME": game_page,
    "MEETING": meeting_page,
    "REVEAL": reveal_page
}

function loadPage(status){
    $( ".page" ).css("display", "none");
    let page = pages[status];
    $( page.selector ).css("display", "block");
    $( "html" ).css("background-color", page.backgroundColor);
    if("update" in page) page.update();
}

function startGame(){
    $.post("command/START_GAME", function(data){
        timeCounter = -1;
        updatePage();
    });
}