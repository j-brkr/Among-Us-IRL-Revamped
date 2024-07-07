
$( document ).ready(function(){
    $.get( "/api/game", function(data){
        console.log(data);
    });

})