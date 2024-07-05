import { settings, getGenero } from "./tienda.js";

let data_idx= localStorage.getItem("idx");
let data;
let cant= 0;
let prod_img;

$(document).ready(function(){

    console.log(data_idx);    
    $.ajax(settings).done(function(response) {
        console.log(response);
        data= response.results[data_idx];   
        console.log("O");
        console.log("L" + data);
        console.log(data.background_image.toString());
        prod_img= document.getElementById("producto-img");
        prod_img.src= data.background_image.toString();
        $("#producto-img").removeClass("skeleton");
        prod_img.style.padding= '0px';
        $("#prod-titulo").text(data.name);
        $("#fecha-prod").append(data.released);
        $("#genre-prod").append(getGenero(response.results[data_idx]));
        $("#rating-prod").append(data.rating);
        document.getElementById("prod-add").value= data_idx; 
    })
    $("#plus").on("click", function(){
        cant= parseInt(document.getElementById("prod-cant").value);
        cant++;
        document.getElementById("prod-cant").value= cant;
        
    })
    $("#minus").on("click", function(){
        cant= parseInt(document.getElementById("prod-cant").value);
        if(cant>1){
            cant--;
            document.getElementById("prod-cant").value= cant;
        }
    })
    $("#prod-add").on("click", function(){
        localStorage.setItem( "cantidad", document.getElementById("prod-cant").value);
    })

})

$("#prod-add").on("click", function(){
    console.log(data_idx);
})