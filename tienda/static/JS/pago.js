import { settings } from "./tienda.js";

const regex= /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
let empty_msg= "No puede dejar este campo vacio";
let data;
let cantidad= localStorage.getItem("cantidad");
let data_idx= localStorage.getItem("idx");


if(regex.test("pedro@yahoo.cl")){
    console.log("Reg ex sirve");
}else{
    console.log("Reg ex NO sirve");
};

$(document).ready(function(){
    let email= $("#emailInput").val();
    let pnombre= $("#nombreInput").val();
    let paterno= $("#paternoInput").val();
    let materno= $("#maternoInput").val();

    $.ajax(settings).done(function (response){
        data= response.results[data_idx];
        document.getElementById("pedido-img").src= (data.background_image).toString();
        $(".pedido-nombre").append(
            (data.name).toString()
        );
        $(".pedido-cant").append(
            cantidad 
        );
        $(".sub-precio").append(
            '<p>$'+ (cantidad * 50990).toString() +'</p>'
        );
        $(".total-precio").append(
            '<p>$'+ (cantidad * 50990).toString() + '</p>'
        );
    })

    $("#emailSmall").css("visibility", "hidden");
    $("#primerSmall").css("visibility", "hidden");
    $("paternoSmall").css("visibility", "hidden");
    $("maternoSmall").css("visibility", "hidden");

    $("#emailSmall").css("color", "red");
    $("#nombreSmall").css("color", "red");
    $("#paternoSmall").css("color", "red");
    $("#maternoSmall").css("color", "red");

    $("#emailInput").on("focusout", function(){
        email= $("#emailInput").val();
        if(email== "" || email == " "){
            document.getElementById("emailSmall").innerHTML= empty_msg;
            $("#emailSmall").css("visibility", "visible");
        }else if(!regex.test(email)){
            document.getElementById("emailSmall").innerHTML= "Debe ingresar un email valido";
            $("#emailSmall").css("visibility", "visible");
        }else{
            console.log("3");
            $("#emailSmall").css("visibility", "hidden");
        }
    });

    $("#paternoInput").on("focusout", function(){
        paterno= $("#paternoInput").val();
        if(paterno== "" || paterno == " "){
            document.getElementById("paternoSmall").innerHTML= empty_msg;
            $("#paternoSmall").css("visibility", "visible");
        }else{
            $("#paternoSmall").css("visibility", "hidden");
        }
    })

    $("#maternoInput").on("focusout", function(){
        materno= $("#maternoInput").val();
        if(materno== "" || materno == " "){
            document.getElementById("maternoSmall").innerHTML= empty_msg;
            $("#maternoSmall").css("visibility", "visible");
        }else{
            $("#maternoSmall").css("visibility", "hidden");
        }

    })


    $("#nombreInput").on("focusout", function(){
        pnombre= $("#nombreInput").val();
        if(pnombre== "" || pnombre == " "){
            $("#nombreInput").val("");
            document.getElementById("nombreSmall").innerHTML= empty_msg;
            $("#nombreSmall").css("visibility", "visible");
        }else{
            $("#nombreSmall").css("visibility", "hidden");
        }
    })



    $("#form-boton").on("click", function(){
        email= $("#emailInput").val();
        materno= $("#maternoInput").val();
        paterno= $("#paternoInput").val();
        pnombre= $("#nombreInput").val();
        console.log(email + " H");

        if(email== "" || email == " "){
            document.getElementById("emailSmall").innerHTML= empty_msg;
            $("#emailSmall").css("visibility", "visible");
        }if(!regex.test(email)){
            document.getElementById("emailSmall").innerHTML= "Debe ingresar un email valido";
            $("#emailSmall").css("visibility", "visible");
        }if(materno== "" || materno== " "){
            document.getElementById("maternoSmall").innerHTML= empty_msg;
            $("#maternoSmall").css("visibility", "visible");
        }
        if(paterno== "" || paterno== " "){
            document.getElementById("paternoSmall").innerHTML= empty_msg;
            $("#paternoSmall").css("visibility", "visible");
        }
        if(pnombre== "" || pnombre==" "){
                $("#nombreInput").val("");
                document.getElementById("nombreSmall").innerHTML= empty_msg;
                $("#nombreSmall").css("visibility", "visible");
        }else{
            alert("Pago realizado con exito");
        }
    });
});



//Revisar

