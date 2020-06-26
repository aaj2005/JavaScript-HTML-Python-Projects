"use strict"
function loadDropDown(){
	let optionRequest = new XMLHttpRequest();
	optionRequest.open("POST" , "/request", true);
	optionRequest.send("loadDropDown")
	optionRequest.onload=function(){
		let startPostResponse=optionRequest.responseText
		startPostResponse=startPostResponse.split(",")
		let selectID = document.getElementById("selector")
		const len= selectID.length
		for(let z=0; z<len;z++){	
			selectID.remove(0)
			
		}
		if(startPostResponse[0]!=""){
			for(let x in startPostResponse){
				let optionSelected = document.createElement("option")
				optionSelected.text = startPostResponse[x] + ".json"
				optionSelected.value = startPostResponse[x]
				selectID.add(optionSelected)
			}
		}	
	}
}
function getName(){
	let onRequest = new XMLHttpRequest();
	onRequest.open("POST" , "/getName", true);
	onRequest.setRequestHeader("Content-type", "text/strings; utf-8");
	onRequest.send(document.getElementById("selector").value)
	onRequest.onload = function() {
		let a=JSON.parse(onRequest.responseText)
		console.log(a)
	};
}
function sendData(){
	let onRequest = new XMLHttpRequest();
	let movieName = document.getElementById("name").value
	let releaseDate = document.getElementById("Date").value
	let review = document.getElementById("rating").value
	let topic = document.getElementById("genre").value
	let postData ={name:movieName,date:releaseDate,rating:review,genre:topic};
	
	onRequest.open("POST" , "/send", true);
	onRequest.setRequestHeader("Content-type", "application/json; utf-8");
	onRequest.send(JSON.stringify(postData))
	
	onRequest.onload = loadDropDown()
}


loadDropDown()