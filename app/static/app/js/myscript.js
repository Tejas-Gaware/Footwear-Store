$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[1]
    console.log("pid =", id)

    $.ajax({
        type:"GET",
        url:"/plus_cart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("data = ",data);
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalAmount").innerText = data.totalAmount
        }
    })
});

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[1]
    console.log("pid =", id)

    $.ajax({
        type:"GET",
        url:"/minus_cart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("data = ",data);
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalAmount").innerText = data.totalAmount
        }
    })
});

$('.remove-cart').click(function(){
    console.log("click")
    var id = $(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"GET",
        url:"/remove_cart",
        data:{
            prod_id:id
        },
        success: function(data){
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalAmount").innerText=data.totalAmount
            eml.parentNode.parentNode.remove()
        }
    })
})