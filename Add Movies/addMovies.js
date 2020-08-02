let movies = [];
let newDate;
let moviesAdded;
mName=document.getElementById("mName") 
description=document.getElementById("desc") 
rating=document.getElementById("rate") 
date=document.getElementById("rDate")

function addMovie(){
	console.log(mName.value)
	if (mName.value==""){
		alert("Please enter a proper name")
		return;
	}
	if (date.value==""){
		alert("Please enter a proper name")
		return;
	}
	if (rating.value==""){
		alert("Please enter a proper name")
		return;
	}
	if (description.value==""){
		alert("Please enter a proper name")
		return;
	}
	
	y=date.value;
	year= y.substr(0,4)
	month= y.substr(5,2)
	day= y.substr(8,2)
	date={
		day:day,
		month:month,
		year:year
	}
	newDate=day+"-"+month+"-"+year
	moviesAdded={
		name:mName.value,
		releaseDate:newDate,
		description:description.value,
		ratings:rating.value
	};
	
	movies.push(moviesAdded)
	mName.value= ""
	description.value= ""
	rating= ""
	date= ""
	a()
}
function a(){
	console.log(moviesAdded.releaseDate)
}*/
