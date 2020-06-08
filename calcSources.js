"use strict";
let value=[];
let operator=[];
let finalVal=0;
let valLastElem;
const displayInput=document.getElementById("display")
let array;


	//Operations
function removeOpCount(tempOp){
			if(value[valLastElem]=="+"){
				value.pop()
				value.push(tempOp)
				document.getElementById("display").value= value.join('')
				console.log(operator)
				operator.pop()
				operator.push(tempOp)
			}else if(value[valLastElem]=="-"){
				value.pop()
				value.push(tempOp)
				document.getElementById("display").value= value.join('')
				console.log(operator)
				operator.pop()
				operator.push(tempOp)
			}else if(value[valLastElem]=="/"){
				value.pop()
				value.push(tempOp)
				document.getElementById("display").value= value.join('')
				console.log(operator)
				operator.pop()
				operator.push(tempOp)
			}else if(value[valLastElem]=="*"){
				value.pop()
				value.push(tempOp)
				document.getElementById("display").value= value.join('')
				operator.pop()
				operator.push(tempOp)
			}else{
			value.push(tempOp)
			operator.push(tempOp)
			document.getElementById("display").value= value.join('')	
			}
}	
	
function add(){
		if(value.length>0){
			valLastElem= value.length-1
			removeOpCount("+")
			console.log(operator)
				
		}
	}

	
function sub(){
		if(value.length>0){
			valLastElem= value.length-1
			removeOpCount("-")
			console.log(operator)
	}
}

	
function mul(){
	if(value.length>0){
		valLastElem= value.length-1
		removeOpCount("*")
		console.log(operator)
	}
}
function div(){
	if(value.length>0){
		console.log(value[-1])
		valLastElem= value.length-1
		removeOpCount("/")
		console.log(operator)
	}
}
	
	function erase(){
		valLastElem= value.length-1
		if(displayInput.value==0){
			displayInput.value=displayInput.defaultValue
		}
		if(displayInput.value.length==1){
			if(displayInput.value==0){
			}else{
				value.pop()
				displayInput.value=0
			}
		}else if(value[valLastElem]=="+"){
			console.log("erased")
			addition--
			value.pop()
			operator.pop()
			console.log("Si")
			document.getElementById("display").value= value.join('')
		}else if(value[valLastElem]=="-"){
			console.log("erased")
			subtraction--
			value.pop()
			operator.pop()
			document.getElementById("display").value= value.join('')
		}else if(value[valLastElem]=="/"){
			console.log("erased")
			division--
			value.pop()
			operator.pop()
			document.getElementById("display").value= value.join('')
		}else if(value[valLastElem]=="*"){
			console.log("erased")
			multiplication--
			value.pop()
			operator.pop()
			document.getElementById("display").value= value.join('')
		}else{
			console.log("erased")
			console.log(value)
			value.pop()
			operator.pop()
			document.getElementById("display").value= value.join('')
			console.log(displayInput.value)
	}
}
	
	
	//Numerical Values


	function n0(){
		value.push(0)
		document.getElementById("display").value= value.join('')
		console.log(displayInput.value)
	}
	function n1(){
		value.push(1)
		document.getElementById("display").value= value.join('')
		console.log(displayInput.value)
	}
	function n2(){
		value.push(2)
		document.getElementById("display").value= value.join('')
		console.log(displayInput.value)
	}
	function n3(){
		value.push(3)
		document.getElementById("display").value= value.join('')
		console.log(displayInput.value)
	}
	function n4(){
		value.push(4)
		document.getElementById("display").value= value.join('')
		console.log(displayInput.value)
	}
	function n5(){
		value.push(5)
		document.getElementById("display").value= value.join('')
		console.log(displayInput.value)
	}
	function n6(){
		value.push(6)
		document.getElementById("display").value= value.join('')
		console.log(displayInput.value)
	}
	function n7(){
		value.push(7)
		document.getElementById("display").value= value.join('')
		console.log(displayInput.value)
	}
	function n8(){
		value.push(8)
		document.getElementById("display").value= value.join('')
		console.log(displayInput.value)
	}
	function n9(){
		value.push(9)
		document.getElementById("display").value= value.join('')
		console.log(displayInput.value)	
	}
	function clearDisplay(){
		value=[]
		operator=[]
		displayInput.value= 0
		finalVal=0
		array=[]
	}
	
	
	
	//EQUALS
function addEquals(value1,value2){
	return value1+value2
}
function subtractEquals(value1,value2){
	return value1-value2
}
function divideEquals(value1,value2){
	return value1/value2
}
function multiplyEquals(value1,value2){
	return value1*value2
}

function equal(){
	valLastElem= value.length-1
	if(value[valLastElem]=="+"||value[valLastElem]=="-"||value[valLastElem]=="*"||value[valLastElem]=="/"){
		alert("Incomplete Expression")
	}else{
		array = value.join("")
		const regexAS=/[+-]/g
		const regexMD=/[*/]/g
		const regexAll=/[*/+-]/g
		console.log(value)
		array=array.split(regexAll)
		console.log(array)
		console.log(operator)
		const counter=array.slice(0)
		for(let i=0;i<counter.length;i++){
			let mLoc=operator.indexOf("*");
			let dLoc=operator.indexOf("/");
			let pos=Math.min(mLoc,dLoc)
			if(mLoc==-1){
				pos=dLoc
			}else if(dLoc==-1){
				pos=mLoc
			}
			switch(operator[pos]){
				case "*":
					array[pos]=multiplyEquals(array[pos],array[pos+1])
					array.splice(pos+1,1)
					operator.splice(pos,1)
					break;
				case "/":
					array[pos]=divideEquals(array[pos],array[pos+1])
					array.splice(pos+1,1)
					operator.splice(pos,1)
					break;
			}
			if(array.includes("*")||array.includes("/")){
				continue
			}else{
				console.log(array, operator)
				for(const x of array){
					let aLoc=operator.indexOf("+");
					let sLoc=operator.indexOf("-");
					let pos=Math.min(sLoc,aLoc)
					console.log(aLoc,sLoc,pos)
					if(aLoc==-1){
						pos=sLoc
					}else if(sLoc==-1){
						pos=aLoc
					}
					switch(operator[pos]){
					case "+":
						array[pos]=addEquals(parseInt(array[pos]),parseInt(array[pos+1]))
						array.splice(pos+1,1)
						operator.splice(pos,1)
						break;
					case "-":
						array[pos]=subtractEquals(parseInt(array[pos]),parseInt(array[pos+1]))
						array.splice(pos+1,1)
						operator.splice(pos,1)
						break;
					}
				}
			}
		}
		console.log(array[0])
		document.getElementById("result").value=array[0]
	}
}				
