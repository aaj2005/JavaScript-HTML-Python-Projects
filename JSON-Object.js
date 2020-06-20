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
	if(key!=""&&property!=""){
		onRequest.open("POST" , "/", true);
		onRequest.setRequestHeader("Content-type", "application/json; utf-8");
		onRequest.send(JSON.stringify(postData))
	}else{
		alert("Please input a proper value")
	}
}
