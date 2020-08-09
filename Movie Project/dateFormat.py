
def checkDate(movieDataInDict,x):
	month=datetime.today().strftime('%m')
	day=datetime.today().strftime('%d')
	year=datetime.today().strftime('%y')
	if movieDataInDict[x][2:4] >= year:
		if movieDataInDict[x][2:4] == year:
			if movieDataInDict[x][5:7] >= month:
				if movieDataInDict[x][5:7] == month:
					if movieDataInDict[x][8:] >= day:
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
def checkDateFormat(movieDataInDict,x,withDate):
	error=False
	noError=True
	compiled= re.compile("[0-9]{4}\-[0-9]{2}\-[0-9]{2}")
	continueCheck=True
	if continueCheck:
		if compiled.match(movieDataInDict[x]) is not None:
			if movieDataInDict[x][5] <='1':
				if movieDataInDict[x][5] =='1':
					if movieDataInDict[x][6] <='2':
						if movieDataInDict[x][6]== '2' or movieDataInDict[x][6]== '0':
							if movieDataInDict[x][0:4]!= "0000" and movieDataInDict[x][8:]>= "00" and movieDataInDict[x][8:]<="31":
								return noError
							else:
								return error
						elif movieDataInDict[x][6]=='1':
							if movieDataInDict[x][0:4]!= "0000" and movieDataInDict[x][8:]>= "00" and movieDataInDict[x][8:]<="30":
								return noError
							else:
								return error
						else:
							return error
					else:
						return error
				elif movieDataInDict[x][5] == '0' and movieDataInDict[x][6] != '0':
					if movieDataInDict[x][5:7] in ('04','06','09','11'):  
						if movieDataInDict[x][8:] <='30' and movieDataInDict[x][8:]>'00':
							if movieDataInDict[x][0:4]!= "0000":
								return noError
							else:
								return error
						else:
							return error
					elif movieDataInDict[x][5:7] in ('01','03','05','07','08','10','12'):
						if movieDataInDict[x][8:] <='31' and movieDataInDict[x][8:]>'00':
							if movieDataInDict[x][0:4]!= "0000":
								return noError
							else:
								return error
					elif movieDataInDict[x][5:7] == '02':
						if int(movieDataInDict[x][0:4]) %4 == 0 and int(movieDataInDict[x][0:4]) %100 ==0 and int(movieDataInDict[x][0:4]) %400 == 0:
							
							if movieDataInDict[x][8:] <='29' and movieDataInDict[x][8:]>'00':
								if movieDataInDict[x][0:4]!= "0000":
									return noError
								else:
									return error
							else:
								return error
						elif movieDataInDict[x][8:] <='28' and movieDataInDict[x][8:]>'00':
							if movieDataInDict[x][0:4]!= "0000":
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
	else:
		return error
