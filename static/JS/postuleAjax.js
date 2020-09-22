$(document).ready(function(){
    $("#contactForm").submit(function(e){
        // prevent from normal form behavior
        e.preventDefault();
        // serialize the form data
        var serialiseData = $(this).serialize();

        $.ajax({
            
            type : 'POST',
           
            url : $(this).attr('action'),
          
            data : serialiseData,
            success : function(response){
                // reset the form after successful submit 
                console.log(responseText);
            },
            error : function(response){
                console.log(response);
            }
        })
    })
})