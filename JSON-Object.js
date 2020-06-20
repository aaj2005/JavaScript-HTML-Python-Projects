"use strict"
function getName(){
	let onRequest = new XMLHttpRequest();
	onRequest.open("GET" , "/home", true);
	onRequest.send()
	onRequest.onload = function() {
		let a=JSON.parse(onRequest.responseText)
		console.log(a)
	};
}
function sendData(){
	let onRequest = new XMLHttpRequest();
	let key = document.getElementById("key").value
	let property = document.getElementById("property").value
	console.log(key,property)
	let postData ={};
	postData[key]=property
	console.log(postData)
	console.log(onRequest.readyState)
	onRequest.open("POST" , "/", true);
	onRequest.setRequestHeader("Content-type", "application/json; utf-8");
	onRequest.send(JSON.stringify(postData))
}
