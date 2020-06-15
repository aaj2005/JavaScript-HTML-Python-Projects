"use strict"
function getName(){
	let onRequest = new XMLHttpRequest();
	onRequest.open("GET" , "http://localhost:1234/JSON-Object.json", true);
	onRequest.send()
	onRequest.onload = function() {
		let x= JSON.parse(onRequest.responseText)
		document.getElementById("demo").innerHTML = x.name
	};
}