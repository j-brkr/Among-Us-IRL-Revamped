let timeCounter = -1;
let page = "MEETING";
let discussion_time = 300;

$( document ).ready(function(){
    checkStatus();
    setInterval(checkStatus, 1000);
});

function checkStatus(){
    $.get( "/api/game", function(game){
        console.log(game["status"]);
        if(page.status != game["status"]){
            loadPage(game["status"]);
        }
        page.update();
    })
    .fail(function(jqXHR, textStatus, errorThrown){
        console.log(JSON.stringify(jqXHR));
        document.write("GET Failed. The server is probably down\n")
    });
}

const lobby_page = {
    status: "LOBBY",
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
    game: "REVEAL",
    selector: "#role-reveal",
    backgroundColor: "black",
    update: function(){
        timeCounter++;
        console.log("Reveal update" + timeCounter);
        if(timeCounter === 0){
            audio = $( "#revealAudio" )[0];
            audio.play();
        }
        if(timeCounter === 8){
            // Reveal time is up
            $.post("/command/END_REVEAL", function(data){
                //alert(data);
                checkStatus();
            });
        }
    }
}

const game_page = {
    status: "GAME",
    selector: "#game",
    backgroundColor: "#264775"
}

const meeting_page = {
    status: "MEETING",
    selector: "#voting",
    backgroundColor: "rgb(0 177 255)",
    load: function(){
        location.reload();
    },
    update: function(){
        discussion_time--;
        $( "#discussionTimer" ).html("Discussion Time: " + Math.floor(discussion_time/60) + ":" + discussion_time%60);
    }
}

const crew_win_page = {
    status: "CREW_WIN",
    selector: "#crewWin",
    backgroundColor: "rgb(0 0 0)"
}

const imposter_win_page = {
    status: "IMPOSTER_WIN",
    selector: "#imposterWin",
    backgroundColor: "rgb(0 0 0)"
}

const pages={
    "LOBBY": lobby_page,
    "GAME": game_page,
    "MEETING": meeting_page,
    "REVEAL": reveal_page,
    "CREW_WIN": crew_win_page,
    "IMPOSTER_WIN": imposter_win_page
}

function loadPage(status){
    $( ".page" ).css("display", "none");
    let page = pages[status];
    $( page.selector ).css("display", "block");
    $( "html" ).css("background-color", page.backgroundColor);
    //if("load" in page) page.load();
    if("update" in page) page.update();
}

function startGame(){
    $.post("command/START_GAME", function(data){
        timeCounter = -1;
        checkStatus();
    });
}

function emergencyPressed(){
    $.post("command/EMERGENCY", function(data){
        checkStatus();
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
    let impCount = -1;
    let text = "DEFAULT";
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
    $( "#ejectText" ).empty();
    $( "#eject" ).css("display", "block");
    $( "#eject" ).css("opacity", "1");
    setTimeout(ejectMessage, 1500, text);
    setTimeout(impostersRemaining, 5000, impCount);
    setTimeout(function(){
        $.post("command/EJECTED", function(data){
            $( "#eject" ).css("opacity", "0");
            checkStatus();
        });
    }, 7000);
    setTimeout(function(){$( "#eject" ).css("display", "none")}, 8000);
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

function endGame(){
    $.post("command/END_GAME", function(data){
        checkStatus();
    });
}