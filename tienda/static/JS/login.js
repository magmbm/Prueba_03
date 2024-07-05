
const regex= /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
let empty_msg= "No puede dejar este campo vacio";

$(document).ready(function(){
    let nombre= $("#nombre_usuario").val();
    let contra= $("#contra_usuario").val();


    $("#contra_small").css("color", "red");
    $("#nombre_small").css("color", "red");

    $("#nombre_usuario").on("focusout", function(){
        nombre= $("#nombre_usuario").val();
        if(nombre== "" || nombre == " "){
            document.getElementById("nombre_small").innerHTML= empty_msg;
            $("#nombre_small").css("visibility", "visible");
        }else{
            $("#nombre_small").css("visibility", "hidden");
        }
    })

    $("#contra_usuario").on("focusout", function(){
        contra= $("#contra_usuario").val();
        if(contra== "" || contra == " "){
            document.getElementById("contra_small").innerHTML= empty_msg;
            $("#contra_small").css("visibility", "visible");
        }else{
            $("#contra_small").css("visibility", "hidden");
        }
    })
})