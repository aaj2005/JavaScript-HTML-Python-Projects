"use strict"
let profName
async function getProfName(){
	profName=await fetch('/getProfName',{method : 'GET', headers:{'Content-Type':'text/plain'}});
	profName =await profName.text()
	document.getElementById('h1Prof').innerHTML="Welcome "+profName
	addToTable('myMenu','/getMovieName')
	addToTable('myMenuList','/getList')
}
let accName
async function getAccName(){
	accName=await fetch('/getAccName',{method : 'GET', headers:{'Content-Type':'text/plain'}});
	accName =await accName.text()
}
getAccName()
getProfName()



let newList =[]
let responseArray=[]
let objectList={}
let listResponseArray=[]

function addToTable(ulName,tableToRetrieve,clickedElement= 1){
	console.log(clickedElement)
	responseArray=[]
	objectList={}
	listResponseArray=[]
	let ul= document.getElementById(ulName) 
	ul.innerHTML = ''
	
	let sendMethod='GET' 
	if (tableToRetrieve =="/getList"){
		sendMethod='POST'
	}
	let onRequest = new XMLHttpRequest();
	onRequest.open(sendMethod , tableToRetrieve, true);
	onRequest.setRequestHeader("Content-type", "text/plain; utf-8");
	if (tableToRetrieve=='/getList'){
		onRequest.send(accName+','+profName)
	}else{
		onRequest.send()
	}
	onRequest.onload = function(){
		let movieNames=onRequest.responseText.split([','])
		for (let pos in movieNames){
			movieNames[pos]=movieNames[pos].split([':'])
		}
		for(let i=1;i<=movieNames.length;i++){
			let request = new XMLHttpRequest();
			request.open("POST" , "/getShowData", true);
			request.setRequestHeader("Content-type", "text/strings; utf-8");
			request.send(i)
			request.onload = function() {
				let movieATag = document.createElement("a");
				let addToList = document.createElement("a");
				let li=document.createElement("li")
				let inJSON=request.responseText.split(',')
				movieATag.textContent=movieNames[i-1][0]
				movieATag.setAttribute("onClick",'on("'+ulName+'")')
				movieATag.classList.add('left')
				li.appendChild(movieATag)
				if (ulName=='myMenu'){
					objectList[inJSON[1].slice(1)]=i
					responseArray.push(inJSON)
					addToList.textContent= '+'
					addToList.setAttribute('id',inJSON[1].slice(1))
					addToList.setAttribute("onClick",'addToList(this.id)')
					addToList.classList.add('right')
				}else{
					if (movieNames!=''){
						listResponseArray.push(movieNames[i-1][0])
					}else{
						listResponseArray.push('')
					}
				}
				li.appendChild(addToList)
				ul.appendChild(li)
				li.classList.add('myMenu')
			}
			setTimeout(function(){
				for (let x in listResponseArray){
					document.getElementById(listResponseArray[x]).innerHTML= '-'
				}
					
				
			}, 100);
			
		}		
	}	
}

		
async function logout(){
	let logout=await fetch('/logout',{method : 'GET', headers:{'Content-Type':'application/json'}});
	window.location.replace("/login.html")
}



    



function getEventTarget(e) {
    e = e || window.event;
    return e.target || e.srcElement; 
}

function on(ulName) {
	let imageTag = document.getElementById("overlayImg")
	let overlay = document.getElementById("overlay")
	let imgRequest= new XMLHttpRequest()
	let ul = document.getElementById(ulName);
	ul.onclick = function(event) {	
		let target = getEventTarget(event).innerHTML;
		imgRequest.open("POST" , "/loadImg", true);
		imgRequest.setRequestHeader("Content-type", "text/strings; utf-8");
		imgRequest.send(objectList[target])
		imgRequest.onload= function(){		
			imageTag.src= "/loadImg"
			overlay.style.display = "flex";
			imageTag.style.display= "flex"
			imageTag.addEventListener("click",function(){
				imgRequest.setRequestHeader("Content-type", "text/strings; utf-8")
				imgRequest.send(objectList[target])
				imgRequest.onload= function(){
					imageTag.style.display= "none"


				}
			})
		}
	}
}
	
document.addEventListener("keydown",function(){
	if(event.key=="Escape"&& document.getElementById("overlay").style.display == "flex"){
		document.getElementById("overlay").style.display = "none";
		document.getElementById("overlayImg").style.display= "none"
	}
})

async function addToList(movieID){

	let bodyContent=JSON.stringify([movieID,accName,profName])
	let addToList=await fetch('/addToList',{method : 'POST', headers:{'Content-Type':'application/json'},body:bodyContent});
	addToList =await addToList.text()
	let aTag=document.getElementById(addToList).innerHTML
	addToTable('myMenu','/getMovieName')
	addToTable('myMenuList','/getList',addToList)

}

function myFunction(htmlUL,searchInput) {
	let x, input, filter, ul, li, a, i,genre ;
	let movieOnDict={}
	input = document.getElementById(searchInput);
	filter = input.value.toUpperCase();
	ul = document.getElementById(htmlUL);
	li = ul.getElementsByTagName("li");
	// Loop through all list items, and hide those who don't match the search query
	
	for (i = 0; i < li.length; i++) {
		if (searchInput=='myList'){
			responseArray=listResponseArray
		}
		for(x in responseArray){
			genre = responseArray[x][3].slice(1)
			a = li[x].getElementsByTagName("a")[0];
			if (genre.toUpperCase().indexOf(filter) > -1 ||a.innerHTML.toUpperCase().indexOf(filter) > -1){
			  li[x].style.display = "";
			} else {
			  li[x].style.display = "none";
			
			}
		}
	}
}