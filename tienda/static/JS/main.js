import { settings } from "./tienda.js";

export function insertGameNames(data, target_id){
    $.each(data.results, function(i, item){
        $("#" + target_id).append(
            "<option value='" + item.name +"' >" + item.name +"</option>"
        );
    })
}

$(document).ready(function(){
    $.ajax(settings).done(function (response) {
        insertGameNames(response, "lista_de_juegos");
    });
})

