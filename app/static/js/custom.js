    document.getElementById("id_shop_name").required = false;
    document.getElementById("id_docs").required = false;
function checkRole(answer) {

  console.log(answer)
  if (answer == "thisshop") { // hide the div that is not selected

    document.getElementById('thisshop').style.display = "block";
    // document.getElementById("id_shop_name").required = true;
    // document.getElementById("id_docs").required = true;
  } else{

    document.getElementById('thisshop').style.display = "none";

  }

}
