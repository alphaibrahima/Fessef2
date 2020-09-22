var loader = function(e){
    let file = e.target.files
    let output = document.getElementById("selector");
    //
    if (file[0].type.match("image")){
      //si le fichier est un image
      let reader = new FileReader();
      reader.addEventListener("load", function(e){
        let data = e.target.result;
        let image = document.createElement("img");
        image.src = data;
        output.innerHTML = "";
        output.insertBefore(image, null);
        output.classList.add("image");

      });
      reader.readAsDataURL(file[0]);
    }else{
      //si le fichier n'est pas un image

      //Pour afficher le nom du fichier dans le label
      let show = "<span>Nom de fichier : </span>"+file[0].name;
      output.innerHTML = show;
      output.classList.add("active");


      if(output.classList.contains("image")){
        output.classList.remove("image");
      }
    }

  };
  //Ajouter un evenement 
  let fileInput = document.getElementById("thumbnail");
  fileInput.addEventListener("change", loader)



