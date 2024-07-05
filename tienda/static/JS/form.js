import { settings } from "./tienda.js";

const regex= /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:.[a-zA-Z0-9-]+)$/

$(document).ready(function(){
    let email= $("#emailInput").val();
    let asunto= $("#asunInput").val();
    let mensaje= $("#mensInput").val();
    let empty_msg= "No puede dejar esta campo vacio"

    $("#emailSmall").css("color", "red");
    $("#asunSmall").css("color", "red");
    $("#mensSmall").css("color", "red");

    $("#emailInput").on("focusout", function(){
        email= $("#emailInput").val();
        if(email== "" || email == " "){
            document.getElementById("emailSmall").innerHTML= empty_msg;
            $("#emailSmall").css("visibility", "visible");
        }else if(!regex.test(email)){
            document.getElementById("emailSmall").innerHTML= "Debe ingresar un email valido";
            $("#emailSmall").css("visibility", "visible");
        }else{
            $("#emailSmall").css("visibility", "hidden");
        }
    });

    $("#asunInput").on("focusout", function(){
        asunto= $("#asunInput").val();
        if(asunto== "" || asunto == " "){
            document.getElementById("asunSmall").innerHTML= empty_msg;
            $("#asunSmall").css("visibility", "visible");
        }else if(!regex.test(email)){
            document.getElementById("asunSmall").innerHTML= "Debe escribir un asunto";
            $("asunSmall").css("visibility", "visible");
        }else{
            $("#asunSmall").css("visibility", "hidden");
        }
    });

    $("#mensInput").on("focusout", function(){
        mensaje= $("#mensInput").val();
        if(mensaje== "" || mensaje == " "){
            document.getElementById("mensSmall").innerHTML= empty_msg;
            $("#mensSmall").css("visibility", "visible");
        }else if(!regex.test(email)){
            document.getElementById("mensSmall").innerHTML= "Debe escribir un asunto";
            $("mensSmall").css("visibility", "visible");
        }else{
            $("#mensSmall").css("visibility", "hidden");
        }
    });

    $("#contactar-btn").on("click", function(){
        email= $("#emailInput").val();
        asunto= $("#asunInput").val();
        mensaje= $("#mensInput").val();
        if(mensaje== "" || mensaje == " "){
            document.getElementById("mensSmall").innerHTML= empty_msg;
        }if(email== "" || email == " "){
            document.getElementById("emailSmall").innerHTML= empty_msg;
            $("#emailSmall").css("visibility", "visible");
        }if(asunto== "" || asunto == " "){
            document.getElementById("asunSmall").innerHTML= empty_msg;
            $("#asunSmall").css("visibility", "visible");
        }else{
            alert("Mensaje enviado con exito")
        }
    })


});