$(document).ready(function(){

    $(".delete").click(function(e){
        var id = this.id; //$(this).attr('id);
        var href = this.href; 
        console.log(href, id) //recuper le href du lien
        e.preventDefault(); //don't follow the link
    
        $.ajax({
            url: href,
            data: {},
        });
    
        $("#"+id).fadeOut(1000);
    });
    
})



