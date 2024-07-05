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
        cell.on( "click", buttonFunc(buttonText[i]));
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

function buttonFunc(name){
    if(!isNaN(parseInt(name))){ // If a digit
        return appendPinbox(name);
    }
    else if(name === "X"){
        return function clearPinbox(){
            pinInput = "";
            pinDisplay = "";
            $('#pin-box').text(pinDisplay);
        }
    }else if(name === "✓"){
        return function submitNumber(){
            $('#pin').attr("value", pinInput);
            $('form').submit();
        }
    }

    return function(){
        alert( "Handler for " + name + " called." );
    }
}

function submitPin(pin){
    
}