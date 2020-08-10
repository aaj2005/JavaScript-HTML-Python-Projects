#Checks if it is after today
import re
from datetime import datetime

def checkDate(movieDataInDict,theDate):
	month=datetime.today().strftime('%m')
	day=datetime.today().strftime('%d')
	year=datetime.today().strftime('%y')
	if movieDataInDict[theDate][2:4] >= year:
		if movieDataInDict[theDate][2:4] == year:
			if movieDataInDict[theDate][5:7] >= month:
				if movieDataInDict[theDate][5:7] == month:
					if movieDataInDict[theDate][8:] >= day:
						return True
					else:
						return False
				else:
					return True
			else:
				return False
		else:
			return True
	else:
		return False
def checkDateFormat(movieDataInDict,theDate,withDate):
	error=False
	noError=True
	compiled= re.compile("[0-9]{4}\-[0-9]{2}\-[0-9]{2}")
	continueCheck=True
	if compiled.match(movieDataInDict[theDate]) is not None:
		if movieDataInDict[theDate][5] <='1':
			if movieDataInDict[theDate][5] =='1':
				if movieDataInDict[theDate][6] <='2':
					if movieDataInDict[theDate][6]== '2' or movieDataInDict[theDate][6]== '0':
						if movieDataInDict[theDate][0:4]!= "0000" and movieDataInDict[theDate][8:]>= "00" and movieDataInDict[theDate][8:]<="31":
							return noError
						else:
							return error
					elif movieDataInDict[theDate][6]=='1':
						if movieDataInDict[theDate][0:4]!= "0000" and movieDataInDict[theDate][8:]>= "00" and movieDataInDict[theDate][8:]<="30":
							return noError
						else:
							return error
					else:
						return error
				else:
					return error
			elif movieDataInDict[theDate][5] == '0' and movieDataInDict[theDate][6] != '0':
				if movieDataInDict[theDate][5:7] in ('04','06','09','11'):  
					if movieDataInDict[theDate][8:] <='30' and movieDataInDict[theDate][8:]>'00':
						if movieDataInDict[theDate][0:4]!= "0000":
							return noError
						else:
							return error
					else:
						return error
				elif movieDataInDict[theDate][5:7] in ('01','03','05','07','08','10','12'):
					if movieDataInDict[theDate][8:] <='31' and movieDataInDict[theDate][8:]>'00':
						if movieDataInDict[theDate][0:4]!= "0000":
							return noError
						else:
							return error
				elif movieDataInDict[theDate][5:7] == '02':
					if int(movieDataInDict[theDate][0:4]) %4 == 0 and int(movieDataInDict[theDate][0:4]) %100 ==0 and int(movieDataInDict[theDate][0:4]) %400 == 0:
						if movieDataInDict[theDate][8:] <='29' and movieDataInDict[theDate][8:]>'00':
							if movieDataInDict[theDate][0:4]!= "0000":
								return noError
							else:
								return error
						else:
							return error
					elif movieDataInDict[theDate][8:] <='28' and movieDataInDict[theDate][8:]>'00':
						if movieDataInDict[theDate][0:4]!= "0000":
							return noError
						else:
							return error
					else:
						return error
				else:
					return error
			else :
				return error
		else:
			return error
	else:
		return error