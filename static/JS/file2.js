// evenement sur le cv 
var loader2 = function(e){
    let file2 = e.target.files;
    let show2 = "<span>Nom de fichier : </span>"+file2[0].name;
    let output2 = document.getElementById("selector2");
    output2.innerHTML = show2;
    output2.classList.add("active");
};

// add event 
let fileInput2 = document.getElementById("curiculum")
fileInput2.addEventListener("change", loader2)
  


