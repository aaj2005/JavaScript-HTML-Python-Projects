'use strict'
document.getElementById('add').addEventListener('click',function(){document.getElementById("overlay").style.display="flex"})

async function getAccName(){
	
	const response=await fetch('/getAccName',{method : 'GET', headers:{'Content-Type':'text/plain'}});
	let x =await response.text()
	document.getElementById('nameOfAccount').innerHTML = x
}
getAccName()