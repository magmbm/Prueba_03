
let data;
let cant= 0;
let prod_img;

$(document).ready(function(){

    console.log(data_idx);    
    $("#plus").on("click", function(){
        cant= parseInt(document.getElementById("prod-cant").value);
        cant++;
        document.getElementById("prod-cant").value= cant;
        console.log("Prueba");
        
    })
    $("#minus").on("click", function(){
        cant= parseInt(document.getElementById("prod-cant").value);
        if(cant>1){
            cant--;
            document.getElementById("prod-cant").value= cant;
        }
    })

})
