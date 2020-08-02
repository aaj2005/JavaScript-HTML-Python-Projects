"use strict"
let videoTag= document.getElementById("video")
let responseArray=[]
let objectList={}
let onRequest = new XMLHttpRequest();
onRequest.open("GET" , "/getArrayCount", true);
onRequest.setRequestHeader("Content-type", "text/strings; utf-8");
onRequest.send()
onRequest.onload = function(){
	for(let i=1;i<=onRequest.responseText;i++){
		let request = new XMLHttpRequest();
		request.open("POST" , "/getName", true);
		request.setRequestHeader("Content-type", "text/strings; utf-8");
		request.send(i)
		request.onload = function() {
			let a = document.createElement("a");
			let ul= document.getElementById("myMenu")
			let li=document.createElement("li")
			let inJSON=request.responseText.split(',')
			objectList[inJSON[1]]=i
			responseArray.push(inJSON)
			a.textContent=inJSON[1]
			a.setAttribute("onClick","on()")
			li.appendChild(a)
			ul.appendChild(li)				
			li.classList.add("myMenu")
		};
	}		
}
function getEventTarget(e) {
    e = e || window.event;
    return e.target || e.srcElement; 
}

function on() {
	let imageTag = document.getElementById("overlayImg")
	let overlay = document.getElementById("overlay")
	let imgRequest= new XMLHttpRequest()
	let ul = document.getElementById('myMenu');
	ul.onclick = function(event) {
		let target = getEventTarget(event).innerHTML;
		imgRequest.open("POST" , "/loadImg", true);
		imgRequest.setRequestHeader("Content-type", "text/strings; utf-8");
		imgRequest.send(objectList[target])
		imgRequest.onload= function(){		
			imageTag.src= "/loadImg"
			overlay.style.display = "flex";
			videoTag.style.display = "none";
			imageTag.style.display= "flex"
			imageTag.addEventListener("click",function(){
				imgRequest.open("POST", "/loadVid", true)
				imgRequest.setRequestHeader("Content-type", "text/strings; utf-8")
				imgRequest.send(objectList[target])
				imgRequest.onload= function(){
					imageTag.style.display= "none"
					videoTag.style.display= "flex"
					videoTag.src="/loadVid"


				}
			})
		}
	}
}
let videoStatus = false
videoTag.addEventListener("click",function(){
	if(videoStatus==false || videoTag.paused){
		videoTag.play()
		videoStatus= true
		console.log(videoTag.seekable.end(0))
	}else{
		videoTag.pause()
		videoStatus = false
		
	}
	
	})
	
document.addEventListener("keydown",function(){
	if(event.key=="Escape"&& document.getElementById("overlay").style.display == "flex"){
		document.getElementById("overlay").style.display = "none";
		document.getElementById("overlayImg").style.display= "none"
		document.getElementById("video").src=""
	}
})



function myFunction() {
	let x, input, filter, ul, li, a, i,genre;
	input = document.getElementById("mySearch");
	filter = input.value.toUpperCase();
	ul = document.getElementById("myMenu");
	li = ul.getElementsByTagName("li");
	
	for(x in responseArray){
		genre = responseArray[x]["genre"]
		a = li[x].getElementsByTagName("a")[0];
		if (genre.toUpperCase().indexOf(filter) > -1) {
		  li[x].style.display = "";
		} else {
		  li[x].style.display = "none";
		}
		x++
	}

	// Loop through all list items, and hide those who don't match the search query
	for (i = 0; i < li.length; i++) {
		a = li[i].getElementsByTagName("a")[0];
		if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
			li[i].style.display = "";
		} else {
			if(li[i].style.display!="none"){
				continue
			}else{
			li[i].style.display = "none";
			}
		}
	}
}
