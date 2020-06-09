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
				operator.pop()
				operator.push(tempOp)
			}else if(value[valLastElem]=="-"){
				value.pop()
				value.push(tempOp)
				document.getElementById("display").value= value.join('')
				operator.pop()
				operator.push(tempOp)
			}else if(value[valLastElem]=="/"){
				value.pop()
				value.push(tempOp)
				document.getElementById("display").value= value.join('')
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
				
		}
	}

	
function sub(){
		if(value.length>0){
			valLastElem= value.length-1
			removeOpCount("-")
	}
}

	
function mul(){
	if(value.length>0){
		valLastElem= value.length-1
		removeOpCount("*")
	}
}
function div(){
	if(value.length>0){
		valLastElem= value.length-1
		removeOpCount("/")
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
			value.pop()
			operator.pop()
			document.getElementById("display").value= value.join('')
		}else if(value[valLastElem]=="-"){
			value.pop()
			operator.pop()
			document.getElementById("display").value= value.join('')
		}else if(value[valLastElem]=="/"){
			value.pop()
			operator.pop()
			document.getElementById("display").value= value.join('')
		}else if(value[valLastElem]=="*"){
			value.pop()
			operator.pop()
			document.getElementById("display").value= value.join('')
		}else{
			value.pop()
			operator.pop()
			document.getElementById("display").value= value.join('')
	}
}
	
	
	//Numerical Values


	function n0(){
		value.push(0)
		document.getElementById("display").value= value.join('')
	}
	function n1(){
		value.push(1)
		document.getElementById("display").value= value.join('')
	}
	function n2(){
		value.push(2)
		document.getElementById("display").value= value.join('')
	}
	function n3(){
		value.push(3)
		document.getElementById("display").value= value.join('')
	}
	function n4(){
		value.push(4)
		document.getElementById("display").value= value.join('')
	}
	function n5(){
		value.push(5)
		document.getElementById("display").value= value.join('')
	}
	function n6(){
		value.push(6)
		document.getElementById("display").value= value.join('')
	}
	function n7(){
		value.push(7)
		document.getElementById("display").value= value.join('')
	}
	function n8(){
		value.push(8)
		document.getElementById("display").value= value.join('')
	}
	function n9(){
		value.push(9)
		document.getElementById("display").value= value.join('')
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

function equal(value,operator){
	valLastElem= value.length-1
	if(value[valLastElem]=="+"||value[valLastElem]=="-"||value[valLastElem]=="*"||value[valLastElem]=="/"){
		alert("Incomplete Expression")
	}else{
		array = value.join("")
		const regexAS=/[+-]/g
		const regexMD=/[*/]/g
		const regexAll=/[*/+-]/g
		array=array.split(regexAll)
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
				for(const x of array){
					let aLoc=operator.indexOf("+");
					let sLoc=operator.indexOf("-");
					let pos=Math.min(sLoc,aLoc)
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
		return array[0]
	}
}	
function callEqual(){
	document.getElementById("result").value=equal(value,operator)
}
function unitTest(){
	console.log("before")
	assertEQ(2,"1+1")
	assertEQ(2,"1*2/1")
	assertEQ(60,"12-12-12+12*6")
	assertEQ(8082,"672*3*4+5+6*2+1")
	console.log("after")

}
function assertEQ(expected,expression){
	const actual = equal([...expression,],[...expression.replace(/[^-+*/]/g,"")])
	if(expected!==actual){
		console.warn(`Expected ${expression} = ${expected} but got ${actual}`)
	}
}
unitTest()