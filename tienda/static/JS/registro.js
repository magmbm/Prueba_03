

const regex= /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
let empty_msg= "No puede dejar este campo vacio";

$(document).ready(function(){
    let usuario= $("#nombre_usuario").val();
    let contra= $("#contra_usuario").val();
    let nombre= $("#nombre_id").val();
    let pri_apellido= $("#p_apellido").val()
    let seg_apellido= $("#s_apellid").val()
    let email= $("#correo_id").val()



    $("#contra_small").css("color", "red");
    $("#nombre_small").css("color", "red");
    $("#primer_apellido_small").css("color", "red");
    $("#segundo_apellido_small").css("color", "red");
    $("#email_small").css("color", "red");
    $("#user_small").css("color", "red");


    $("#nombre_usuario").on("focusout", function(){
        usuario= $("#nombre_usuario").val();
        if(usuario== "" || usuario == " "){
            document.getElementById("user_small").innerHTML= empty_msg;
            $("#user_small").css("visibility", "visible");
        }else{
            $("#user_small").css("visibility", "hidden");
        }
    })

    $("#nombre_id").on("focusout", function(){
        nombre= $("#nombre_id").val();
        if(nombre== "" || nombre == " "){
            document.getElementById("nombre_small").innerHTML= empty_msg;
            $("#nombre_small").css("visibility", "visible");
        }else{
            $("#nombre_small").css("visibility", "hidden");
        }
    })

    $("#p_apellido").on("focusout", function(){
        pri_apellido= $("#p_apellido").val();
        if(pri_apellido== "" || pri_apellido == " "){
            document.getElementById("primer_apellido_small").innerHTML= empty_msg;
            $("#primer_apellido_small").css("visibility", "visible");
        }else{
            $("#primer_apellido_small").css("visibility", "hidden");
        }
    })


    $("#s_apellido").on("focusout", function(){
        seg_apellido= $("#s_apellido").val();
        if(seg_apellido== "" || seg_apellido == " "){
            document.getElementById("segundo_apellido_small").innerHTML= empty_msg;
            $("#segundo_apellido_small").css("visibility", "visible");
        }else{
            $("#segundo_apellido_small").css("visibility", "hidden");
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


    $("#correo_id").on("focusout", function(){
        email= $("#correo_id").val();
        if(email== "" || email == " "){
            document.getElementById("email_small").innerHTML= empty_msg;
            $("#email_small").css("visibility", "visible");
        }else if(!regex.test(email)){
            document.getElementById("email_small").innerHTML= "Debe ingresar un email valido";
            $("#email_small").css("visibility", "visible");
        }else{
            console.log("3");
            $("#email_small").css("visibility", "hidden");
        }
    })

    $("#boton-registro").on("click", function(){
        usuario= $("#nombre_usuario").val();
        contra= $("#contra_usuario").val();
        nombre= $("#nombre_id").val();
        pri_apellido= $("#p_apellido").val()
        seg_apellido= $("#s_apellid").val()
        email= $("#correo_id").val()


        if(email== "" || email == " "){
            document.getElementById("email_small").innerHTML= empty_msg;
            $("#email_small").css("visibility", "visible");
        }else if(!regex.test(email)){
            document.getElementById("email_small").innerHTML= "Debe ingresar un email valido";
            $("#email_small").css("visibility", "visible");
        }if(contra== "" || contra == " "){
            document.getElementById("contra_small").innerHTML= empty_msg;
            $("#contra_small").css("visibility", "visible");
        }if(seg_apellido== "" || seg_apellido == " "){
            document.getElementById("segundo_apellido_small").innerHTML= empty_msg;
            $("#segundo_apellido_small").css("visibility", "visible");
        }if(nombre== "" || nombre == " "){
            document.getElementById("nombre_small").innerHTML= empty_msg;
            $("#nombre_small").css("visibility", "visible");
        }if(pri_apellido== "" || pri_apellido == " "){
            document.getElementById("primer_apellido_small").innerHTML= empty_msg;
            $("#primer_apellido_small").css("visibility", "visible");
        }if(usuario== "" || usuario == " "){
            document.getElementById("user_small").innerHTML= empty_msg;
            $("#user_small").css("visibility", "visible");
        }else{
            alert("Usuario Registrado con Exito");
        }
    
    })


})