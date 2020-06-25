function u(){
	y=document.getElementById("date").value;
	year= y.substr(0,4)
	month= y.substr(5,2)
	day= y.substr(8,2)
	date={
		day:day,
		month:month,
		year:year
	}
	
	let options= document.getElementById("video").value
	function getSet(){
		
		class Create{
			constructor(num){
				this.year = num.year
				this.month = num.month
				this.day = num.day
			}	
				get PDate(){
					return "dd/mm/yy: " + this.day + "-" + this.month+ "-" + this.year
				}
				set PDate(properFormat){
					this.date=properFormat
				}
				
			
		}
		
		switch(options){
			case "ali":
				let Num1= new Create(date)
				console.log("Ali:",Num1.PDate)
				break;
			case "basel":
				let Num2 = new Create(date)
				console.log("Basel:",Num2.PDate)
				break;
			case "wael":
				let Num3 = new Create(date)
				console.log("Wael:", Num3.PDate)
				break;
		}
		
	}
	getSet()
}
