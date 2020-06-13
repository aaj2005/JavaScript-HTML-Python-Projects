"use strict"

let xhttp = new XMLHttpRequest()
xhttp.onreadystatechange = function() {
	console.log(xhttp.readyState,this.readyState)
	if (this.readyState == 4 && this.status == 200) {
		let myArr = JSON.parse(this.responseText);
		document.getElementById("demo").innerHTML = myArr[0];
  }
};
xhttp.open("GET","JSON-Object.txt", true)
xhttp.send()