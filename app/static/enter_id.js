const buttonText = ["1","2","3","4","5","6","7","8","9","X","0","✓"];
let pinInput = "";
let pinDisplay = "";

// When the document is loaded
$( document ).ready(function() {
    // Numpad
    let numpad = $("#numpad");
    for(let i=0; i<12; i++){
        let cell = $("<div></div>").text(buttonText[i]).attr("class", "cell");
        cell.attr("id", "pin-"+buttonText[i]);
        cell.on( "click", pinpadClick(buttonText[i]));
        numpad.append(cell);
    }
});

function appendPinbox(c){
    return function(){
        pinBox = $('#pin-box');
        if(pinBox.text().length < 4){
            pinInput+= c;
            pinDisplay+= "*"
        }
        pinBox.text(pinDisplay);
    }
}

/**
 * The callback functions for the pinpad
 * @param {string} cellName the name of the button
 * @returns 
 */
function pinpadClick(cellName){
    if(!isNaN(cellName)){ // If a digit
        return appendPinbox(cellName);
    }
    else if(cellName === "X"){
        return function clearPinbox(){
            pinInput = "";
            pinDisplay = "";
            $('#pin-box').text(pinDisplay);
        }
    }else if(cellName === "✓"){
        return function submitNumber(){
            $('#pin').attr("value", pinInput);
            $('form').submit();
        }
    }

    // Default value, this should never run
    return function(){
        alert( "Handler for " + cellName + " called." );
    }
}