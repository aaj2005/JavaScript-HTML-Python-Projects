"use strict"

	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1; //January is 0!
	var yyyy = today.getFullYear();
	 if(dd<10){
			dd='0'+dd
		} 
		if(mm<10){
			mm='0'+mm
		} 

	today = yyyy+'-'+mm+'-'+dd;
	document.getElementById('expiry').setAttribute("min", today);

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
		if(startPostResponse!=""){
			for(let x=1;x<=startPostResponse;x++){
				let optionSelected = document.createElement("option")
				optionSelected.text = x
				optionSelected.value = x
				selectID.add(optionSelected)
			}
		}	
	}
}
let movieDetails;
function getName(){
	let onRequest = new XMLHttpRequest();
	onRequest.open("POST" , "/getName", true);
	onRequest.setRequestHeader("Content-type", "text/strings; utf-8");
	onRequest.send(document.getElementById("selector").value)
	onRequest.onload = function() {
		movieDetails=onRequest.responseText
		movieDetails = movieDetails.split(',')
		console.log(movieDetails)
		document.getElementById("sendMovie").style.display ="none"
		document.getElementById("updateMovie").style.display ="block"
		document.getElementById("name1").value=movieDetails[1].substring(1)
		document.getElementById("release1").value=movieDetails[2].substring(1)
		document.getElementById("category1").value=movieDetails[3].substring(1)
		document.getElementById("runTime1").value=parseInt(movieDetails[4].substring(1))
		document.getElementById("expiry1").value=movieDetails[5].substring(1)
		document.getElementById("restriction1").value=parseInt(movieDetails[6].substring(1))
		
	};
	console.log(movieDetails)
}
function updateData(){
	let onRequest = new XMLHttpRequest();
	let movieName = document.getElementById("name1")
	let releaseDate = document.getElementById("release1")
	let category = document.getElementById("category1")
	let length = document.getElementById("runTime1")
	let expiry = document.getElementById("expiry1")
	let restriction = document.getElementById("restriction1")
	if(movieName.type!="text"){
		alert("Invalid Value for Name")
	}else if(releaseDate.type!="date"){
		alert("Invalid Value for Release Date")
	}else if(category.type!="text"){
		alert("Invalid Value for Category")
	}else if(length.type!="number"){
		alert("Invalid Value for Run Time")
	}else if(expiry.type!="date"){
		alert("Invalid Value for Expiry Date")
	}else if(restriction.type=="number"){
		
		let postData ={id:movieDetails[0],name:movieName.value,date:releaseDate.value,category:category.value,runTime:length.value,expiry:expiry.value,restriction:restriction.value };
		
		onRequest.open("POST" , "/update", true);
		onRequest.setRequestHeader("Content-type", "application/json; utf-8");
		onRequest.send(JSON.stringify(postData))
		
		onRequest.onload = function(){
			loadDropDown()
			if (onRequest.responseText == "True"){
				console.log()
			}else{
				window.alert("Invalid Value")
			}
			
		}
	}
}
function addMovie(){
	document.getElementById("updateMovie").style.display ="none"
	document.getElementById("sendMovie").style.display ="block"
}
function sendData(){
	let onRequest = new XMLHttpRequest();
	let movieName = document.getElementById("name")
	let releaseDate = document.getElementById("release")
	let category = document.getElementById("category")
	let length = document.getElementById("runTime")
	let expiry = document.getElementById("expiry")
	let restriction = document.getElementById("restriction")
	if(movieName.type!="text"){
		alert("Invalid Value for Name")
	}else if(releaseDate.type!="date"){
		alert("Invalid Value for Release Date")
	}else if(category.type!="text"){
		alert("Invalid Value for Category")
	}else if(length.type!="number"){
		alert("Invalid Value for Run Time")
	}else if(expiry.type!="date"){
		alert("Invalid Value for Expiry Date")
	}else if(restriction.type=="number"){
		
		let postData ={name:movieName.value,date:releaseDate.value,category:category.value,runTime:length.value,expiry:expiry.value,restriction:restriction.value };
		
		onRequest.open("POST" , "/send", true);
		onRequest.setRequestHeader("Content-type", "application/json; utf-8");
		onRequest.send(JSON.stringify(postData))
		
		onRequest.onload = function(){
			loadDropDown()
			if (onRequest.responseText == "True"){
				window.alert("Movie Successfully added")
			}else{
				window.alert("Invalid Value")
			}
			
		}
	}
}

loadDropDown()