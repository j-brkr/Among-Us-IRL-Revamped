const buttonText = ["1","2","3","4","5","6","7","8","9","X","0","V"];

// When the document is loaded
$( document ).ready(function() {
    console.log( "ready!" );
    let table = $("<table></table>");
    let i = 0;
    for(let rowID=0; rowID<4; rowID++){
        let row = $("<tr></tr>");
        for(let colID=0; colID<3; colID++){
            let cell = $("<td></td>").text(buttonText[i]);
            row.append(cell)
            i++;
        }
        table.append(row);
    }
    $('#screen').append(table);
});