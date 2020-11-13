$(document).ready(function(){

    // PostFeeds 
    setInterval(function(){
    $.ajax({
        type    : 'GET',
        url     : "feseul/",
        // data    : {},
        
        success : function(response){
            console.log("response")
        },
        
        error: function(response){
            console.log("No DATA");
        }
        
    });
        
    }, 1000);
    
})