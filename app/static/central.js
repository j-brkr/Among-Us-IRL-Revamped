let timeCounter = -1;

$( document ).ready(function(){
    updatePage();
    setInterval(updatePage, 1000);
});

function updatePage(){
    $.get( "/api/game", function(game){
        //console.log(game);
        loadPage(game["status"]);

    })
    .fail(function(jqXHR, textStatus, errorThrown){
        console.log(JSON.stringify(jqXHR));
        document.write("GET Failed. The server is probably down\n")
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
    backgroundColor: "rgb(0 177 255)"
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

function emergencyPressed(){
    $.post("command/EMERGENCY", function(data){
        updatePage();
    });
}

function togglePlayerAlive(playerId, alive){
    playerSetAlive(playerId, alive).then(function(){
        location.reload();
    })
}

async function playerSetAlive(playerId, alive){
    if(playerId==-1) return;
    let player_data = JSON.stringify({"alive": alive});
    let player = await $.ajax({
        url: "/api/player/" + playerId,
        type: 'PUT',
        data: player_data,
        contentType: "application/json",
        success: function (result){
            return result
        }
    });
    return player;
}

function eject(playerId){
    let impCount = "error";
    let text = "DEFAULT EJECT MESSAGE";
    playerSetAlive(playerId, false).then(function(player){
        console.log(player);
        if(playerId == -1){
            text = "No one was ejected";
        }
        else{
            text = player["user"]["name"] + " was " + (player["role"]===1? "an Imposter" : "not an Imposter");
        }
        $.post("/api/game/imposter_count", function(data){
            console.log(data);
            impCount = data["imposter_count"];
            console.log(impCount);
        })
        .always(function(){
            ejectScreen(text, impCount);
        });
    });
}


let i = 1;
let timeInterval;
function ejectScreen(text, impCount){
    $( "#eject" ).css("display", "block");
    $( "#eject" ).css("opacity", "1");
    setTimeout(ejectMessage, 1500, text);
    setTimeout(impostersRemaining, 5000, impCount);
}

function ejectMessage(text){
    $( '#ejectAudio' )[0].play();
    i = 0;
    timeInterval = setInterval(typeEject, 100, text);
}

function typeEject(text){
    $(" #ejectText ").html(text.substring(0,i));
    i++;
    if(i > text.length){
        clearInterval(timeInterval);
    }
}

function impostersRemaining(impCount){
    $(" #ejectText ").append("<br>" + impCount + (impCount===1? " imposter remains":" imposters remain"));
}