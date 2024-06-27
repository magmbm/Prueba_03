let prod_cant;


$(".trash-btn").on("click", function(){
    prod_cant= parseInt($("#carrito-cant").val());
    $("#carrito-cant").val(prod_cant++);

})