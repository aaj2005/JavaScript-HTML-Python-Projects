"use strict"
function getName(){
	let onRequest = new XMLHttpRequest();
	onRequest.open("GET" , "http://127.0.0.1:1234", true);
	onRequest.send()
	onRequest.onload = function() {
		let a=JSON.parse(onRequest.responseText)
		console.log("a")
		console.log(a.Item1)
	};
}
