"use strict"
function loadDropDown(){
	let optionRequest = new XMLHttpRequest();
	optionRequest.open("POST" , "/request", true);
	optionRequest.send("loadDropDown")
	optionRequest.onload=function(){
	
	let startPostResponse=optionRequest.responseText
	let selectID = document.getElementById("selector")
	const len= selectID.length
	for(let z=0; z<len;z++){	
		selectID.remove(0)
		
	}
	for(let x=1; x<=startPostResponse;x++){
		let optionSelected = document.createElement("option")
		optionSelected.text = x + ".json"
		optionSelected.value = x
		selectID.add(optionSelected)
	}
}
}
function getName(){
	let onRequest = new XMLHttpRequest();
	onRequest.open("POST" , "/home", true);
	onRequest.setRequestHeader("Content-type", "text/strings; utf-8");
	onRequest.send(document.getElementById("selector").value)
	onRequest.onload = function() {
		let a=JSON.parse(onRequest.responseText)
	};
}
function sendData(){
	let onRequest = new XMLHttpRequest();
	let key = document.getElementById("key").value
	let property = document.getElementById("property").value
	let postData ={};
	postData[key]=property
	if(key!=""&&property!=""){
		onRequest.open("POST" , "/", true);
		onRequest.setRequestHeader("Content-type", "application/json; utf-8");
		onRequest.send(JSON.stringify(postData))
	}else{
		alert("Please input a proper value")
	}
	onRequest.onload = loadDropDown()
}
loadDropDown()
