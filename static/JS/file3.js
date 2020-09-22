// evenement sur le lm 
var loaderLm = function(e){
    let fileLm = e.target.files;
    let showLm = "<span>Nom de fichier : </span>"+fileLm[0].name;
    let outputLm = document.getElementById("lettre");
    outputLm.innerHTML = showLm;
    outputLm.classList.add("active");
};

// add event 
let fileInputLm = document.getElementById("lm")
fileInputLm.addEventListener("change", loaderLm)