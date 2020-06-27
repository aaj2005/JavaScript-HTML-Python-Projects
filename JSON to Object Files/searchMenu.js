
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
			let inJSON=JSON.parse(request.responseText)
			objectList[inJSON.name]=i
			responseArray.push(inJSON)
			a.textContent=inJSON.name
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
	let imgRequest= new XMLHttpRequest()
	let ul = document.getElementById('myMenu');
	ul.onclick = function(event) {
		let target = getEventTarget(event).innerHTML;
		imgRequest.open("POST" , "/loadImg", true);
		imgRequest.setRequestHeader("Content-type", "text/strings; utf-8");
		imgRequest.send(objectList[target])
		imgRequest.onload= function(){		
			document.getElementById("overlayImg").src= "/loadImg"
			document.getElementById("overlay").style.display = "flex";
		}
	}
}

function off() {
  document.getElementById("overlay").style.display = "none";
}
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
