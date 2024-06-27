import { insertGameNames } from "./main.js";

export const settings = {
	async: true,
	crossDomain: true,
	url: 'https://rawg-video-games-database.p.rapidapi.com/games?key=5d2d49ee1c9a492383db4a282bf3d3de',
	method: 'GET',
	headers: {
		'X-RapidAPI-Key': '9435183804msh6c9379f949be408p1466dbjsn0c1f158cd172',
		'X-RapidAPI-Host': 'rawg-video-games-database.p.rapidapi.com'
	}
};


let busqueda= '';
export let productos= [];
export let product_id= 0;

export function getGenero(data){
    let genero_str= '';
    $.each(data.genres, function(i, item){
        if(i>0){
            genero_str+= ', ';
        }
        genero_str+= item.name;
    })
    return genero_str;
}

function searchByWord(text){
    let palabra= '';
    let word_arr= [];
    let cont= 0;
    for(let i= 0; i<text.length; i++){
        if(text.charAt(i)!= ' '){ 
            palabra+= text.charAt(i);
        }else{
            word_arr[cont]= palabra;
            cont++;
            palabra= '';
        }
    }
    word_arr[cont]= palabra;
    return word_arr;
}

function getIndexOfData(){
    const botonesTienda= document.getElementsByClassName("carta-btn");
    for(let i= 0; i<botonesTienda.length; i++){
        //console.log("Esta id " + botonesTienda[i].id + " tiene eventListener");
        botonesTienda[i].addEventListener("click", function(){
            product_id= (checking_id(botonesTienda[i].id));
            localStorage.setItem("idx", product_id);
            window.location = $('#anch').attr('href');
        })
    }
}

//I need to fetch the numeric id of the button to  work properly
function checking_id(id){
    let result= '';
    result+= id.charAt(0);
    if(!isNaN(id.charAt(1))){
        result+= id.charAt(1);
    }
    return result;
}



$(document).ready(function(){
    try{
        $.ajax(settings).done(function (response) {

            localStorage.setItem("tuerca", response);
            $("#store-display").empty();
            $.each(response.results, function(i, item){
                $("#store-display").append(
                    '<div class="carta">' +
                        '<img src="' + item.background_image +'"alt="Avatar" class="carta-img"> ' +
                        '<div class="card-cont">' +
                            '<div class="upper-cont">'+
                                '<h4 class="my-3"><b>'+ item.name + '</b></h4>' +
                                '<p>'+ getGenero(item) +'</p>' +
                                '<p>$50.990</p>' +
                            '</div>'+
                            '<div class="lower-cont">'+
                                '<button  id="'+ i.toString() + '-store-btn-m" class="btn btn-primary carta-btn" type="button">Ver más</button>' +
                            '</div>'+
                        '</div>' +
                    '</div>'
                );
            }) 
            getIndexOfData();
            $("#tienda-buscador").on("keyup", function(event){
                $("#store-display").empty();
                busqueda= $("#tienda-buscador").val().toLowerCase();
                if(event.key== "Enter"){
                    $.each(response.results, function(i, item){
                        if(busqueda== item.name.toLowerCase()){
                            $("#store-display").append(
                                '<div class="carta">' +
                                    '<img src="' + item.background_image +'"alt="Avatar" class="carta-img"> ' +
                                    '<div class="card-cont">' +
                                        '<div class="upper-cont">'+
                                            '<h4 class="my-3"><b>'+ item.name + '</b></h4>' +
                                            '<p>'+ getGenero(item) +'</p>' +
                                            '<p>$50.990</p>' +
                                        '</div>'+
                                        '<div class="lower-cont">'+
                                            '<button  id="'+ i.toString() + '-store-btn-n" class="btn btn-primary carta-btn" type="button">Ver más</button>' +
                                        '</div>'+
                                    '</div>' +
                                '</div>'

                            );

                            return false;
                        }else{
                            let words= searchByWord(busqueda);
                            console.log("L: " + words.length);
                            for(let y= 0; y < words.length; y++){
                                console.log(words[y]);
                                if(item.name.toLowerCase().includes(words[y])){
                                    $("#store-display").append(
                                    '<div class="carta">' +
                                        '<img src="' + item.background_image +'"alt="Avatar" class="carta-img"> ' +
                                        '<div class="card-cont">' +
                                            '<div class="upper-cont">'+
                                                '<h4 class="my-3"><b>'+ item.name + '</b></h4>' +
                                                '<p>'+ getGenero(item) +'</p>' +
                                                '<p>$50.990</p>' +
                                            '</div>'+
                                            '<div class="lower-cont">'+
                                                '<button  id="'+ i.toString() + '-store-btn-a" class="btn btn-primary carta-btn" type="button">Ver más</button>' +
                                            '</div>'+
                                        '</div>' +
                                    '</div>'
                                );
                                break;
                                } 
                            }
                        } 
                    })
                    getIndexOfData();
                }
                if(busqueda== ""){
                    $.each(response.results, function(i, item){
                        $("#store-display").append(
                            '<div class="carta">' +
                                '<img src="' + item.background_image +'"alt="Avatar" class="carta-img"> ' +
                                '<div class="card-cont">' +
                                    '<div class="upper-cont">'+
                                        '<h4 class="my-3"><b>'+ item.name + '</b></h4>' +
                                        '<p>'+ getGenero(item) +'</p>' +
                                        '<p>$50.990</p>' +
                                    '</div>'+
                                    '<div class="lower-cont">'+
                                        '<button  id="'+ i.toString() + '-store-btn-b" class="btn btn-primary carta-btn" type="button">Ver más</button>' +
                                    '</div>'+
                                '</div>' +
                            '</div>'
                        );
                    })
                    getIndexOfData();
                }
            })

        })
    }catch(err){
        $("#store-display").append(
            "<div class='no-result'>" +
                "<p>Lo sentimos, no pudimos encontrar resultados</p>" +
            "</div>"
        );
    }
});




/*
'<div class="card" style="width: 18rem;">'+
'<img src="..." class="card-img-top" alt="...">'+
'<div class="card-body">' +
'<h5 class="card-title">Card title</h5>' +
'<p class="card-text">Some quick example text to build on the card title and make up the bulk of the  content.</p>' +
'<a href="#" class="btn btn-primary">Go somewhere</a>' +
'</div>' +
'</div>'
*/