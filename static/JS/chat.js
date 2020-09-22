$(document).ready(function(){
    var dataForm = $(".pb") // selection du formulaire
    dataForm.submit(function(event){//debut du fonction quand on envoi les data avec le clique du boutton submit
        event.preventDefault(); // Annuler le fonctionnement par default du navigateur
        console.log("Form isn't sending")

        

        var thisForm = $(this) // Recuperer les datas du formulaire
        var actionEndpoint = thisForm.attr("action"); // Recuperer le lien dans l'attribut action du formulaire
        var httpMethod = thisForm.attr("method"); // Recuperer le method du formulaire
        var formData = thisForm.serialize(); // Recuperer les datas données dans les formuliares

        // Debut d'ajax pour envoyer les datas 
        $.ajax({
            url : actionEndpoint, // url ou on doit traiter
            method : httpMethod, // method envoyé
            data : formData, // Datas à envoyer

            // Si ajax à reussi avec success
            success : function(data){
                console.log('Success');
                //console.log($('#text').val()); // afficher dans le console le message envoyé 
                var dataE = $('#text').val();
                var dataEe = $("#madivv");
                console.log(data);
                $("#madivv").append("<p>" + data + "</p>");
               
            },

            error   : function(){
                console.log("Error");
                console.log(ErrorData);
            }
        })
        // Fin du fonction ajax pour envoyer les datas 
    })

})