'use strict'
document.getElementById('createUser').addEventListener('click',function(){document.getElementById("overlay").style.display="flex"})

async function getAccName(){
	
	const accResponse=await fetch('/getAccName',{method : 'GET', headers:{'Content-Type':'text/plain'}});
	let accName =await accResponse.text()
	document.getElementById('nameOfAccount').innerHTML = "Welcome "+accName
	document.getElementById('accountname').value=accName
	getUsers()
}
getAccName()

async function getUsers(){
	const userResponse=await fetch('/getUsers',{method : 'POST', headers:{'Content-Type':'text/plain'},body:document.getElementById('accountname').value});
	let usersList =await userResponse.text()
	usersList=usersList.split(',')
	for(let user in usersList){
		console.log(usersList)
		if (usersList != ""){
			let usersDiv=document.getElementById('users')
			let button=document.createElement('button')
			let userLabel=document.createElement('label')
			let singleUserDiv = document.createElement('div')
			singleUserDiv.setAttribute("style","display:flex; margin-left:5%; text-align:center;font-size:44px; flex-direction:row; flex-wrap:wrap;")
			usersDiv.appendChild(singleUserDiv) 
			button.setAttribute("id",usersList[user])
			button.setAttribute('name',usersList[user])
			button.setAttribute("onclick", 'searchMenu("'+usersList[user]+'")')
			userLabel.setAttribute('style','width:100%; text-align:center;')
			userLabel.innerHTML=usersList[user]
			singleUserDiv.appendChild(button)
			singleUserDiv.appendChild(userLabel)
			document.getElementById(usersList[user]).innerHTML=usersList[user][0]
			document.getElementById(usersList[user]).setAttribute("style","font-size:100%; width:100%;height: 85%;")
		}
	}
}
async function searchMenu(id){
	let request = new XMLHttpRequest()
	request.open("POST", "/searchMenu", true)
	request.setRequestHeader("Content-type", "text/plain")
	request.send(id)
	window.location.replace("/searchMenu.html")

}
document.addEventListener("keydown",function(){
	if(event.key=="Escape"&& document.getElementById("overlay").style.display == "flex"){
		document.getElementById("overlay").style.display = "none";
	}
})

async function logout(){
	let logout=await fetch('/logout',{method : 'GET', headers:{'Content-Type':'application/json'}});
	window.location.replace("/login.html")
}