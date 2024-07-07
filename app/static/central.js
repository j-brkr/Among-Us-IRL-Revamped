
$( document ).ready(function(){
    $.get( "/api/game", function(data){
        let game = JSON.parse(data);
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

