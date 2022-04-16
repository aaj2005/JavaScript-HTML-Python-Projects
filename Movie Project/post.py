from email.message import EmailMessage
import re
import sys
from get import sendResponse
sys.path.append('database')
import SQLite
from dateFormat import checkDate, checkDateFormat
sys.path.append('C:/Users/alial/Desktop/Programs/Gmail API')
import Gmail
import hashingPasswords
import classes

def insertShows(movieData,showData):
	try:
		newID=SQLite.getMaxValue("showID", "tvShows")[0][0]+1
		if newID >= 1:
			SQLite.insertShows(newID,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction'])
			showData[movieData['name']]=(classes.tvShows(newID,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction']))
	except:
			SQLite.insertShows(1,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction'])
			showData[movieData['name']]=(classes.tvShows(1,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction']))
	return showData
def updateShows(movieData,ID):
	try:
		if int(ID) >= 1:
			SQLite.updateShows(ID,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction'])
			global showData
			showData = SQLite.retrShow()
	except:
			SQLite.insertShows(1,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction'])
			showData.append(classes.tvShows(1,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction']))

def checkMovieData(self,movieDataInDict):
	condition=False
	if type(movieDataInDict) is dict:
		for x in movieDataInDict:
			if x=="name":
				checkMovie=SQLite.retrieveData('tvShows','name',movieName=movieDataInDict[x])
				movieNameLen=len(str(movieDataInDict[x]))
				if movieNameLen>150 or checkMovie!=[]:
					print(checkMovie)
					sendResponse(self,200,'Content-Type','text/plain; utf-8',b'False')
					break
				else:
					pass
			elif x=="date":
				result=checkDateFormat(movieDataInDict,x,False)
				if result:
					checkDate(movieDataInDict,x)
				else:
					sendResponse(self,200,'Content-Type','text/plain; utf-8',b'False')
					break
			elif x=="category":
				categoryLen=len(str(movieDataInDict[x]))
				if categoryLen>150:
					sendResponse(self,200,'Content-Type','text/plain; utf-8',b'False')
					break
				else:
					pass
			elif x=="runTime":
				try:
					int(movieDataInDict[x])
				except:
					sendResponse(self,200,'Content-Type','text/plain; utf-8',b'False')
					break
			elif x=="expiry":
				result=checkDateFormat(movieDataInDict,x,True)
				if result:
					checkDate(movieDataInDict,x)
				else:
					sendResponse(self,200,'Content-Type','text/plain; utf-8',b'False')
					break
			elif x=="restriction":
				try:
					int(movieDataInDict[x]) 
					condition = True
				except:
					sendResponse(self,200,'Content-Type','text/plain; utf-8',b'False')
					break
			elif x=="id":
				movieID= movieDataInDict[x]
				condition = True
				return condition,movieID
			else:
				condition=False
				break
	else:
		sendResponse(self,200,'Content-Type','text/plain; utf-8',b'False')
	return condition

def createNewAccount(self,decodedBody,invalidOption,accountData):
	for x in ('firstName','lastName','dateOfBirth','user','pass','mail','package'):
		arr = re.findall(x,decodedBody)
		if len(arr) > 1:
			if arr[0] != 'mail':
				invalidOption=False
				sendResponse(self,302,'Location','/newAccount.html',b'')
				break
			else:
				pass
		if arr ==[]:
			invalidOption=False
			sendResponse(self,302,'Location','/newAccount.html',b'')
			break
	if invalidOption:
		formPos=[]
		pos=0
		for x in ('firstName','lastName','dateOfBirth','user','pass','mail','package'):
			formPos.append(re.search(x,decodedBody))
			formPos[pos]=formPos[pos].span()
			pos+=1
		formDict={}
		pos=1
		#decoded body == firstname=x&lastname=y .......
		#formPos == [(0,8)=slotNum]
		#decodedBody[slotNum[0]:slotNum[1]]== decodedbody[0:8]
		for slotNum in formPos:
			slotField=decodedBody[slotNum[0]:slotNum[1]]

			if slotNum[1]!= formPos[-1][1]:
				if decodedBody[slotNum[0]:slotNum[1]] =='pass':
					formDict[slotField]=hashingPasswords.hash_password(decodedBody[slotNum[1]+1:formPos[pos][0]-1])
				else:
					formDict[slotField]=decodedBody[slotNum[1]+1:formPos[pos][0]-1]
			else:
				formDict[slotField]=decodedBody[slotNum[1]+1:]
			pos+=1
		for x in formDict:
			formDict[x]=re.sub('\+',' ',formDict[x])
		
		userCompare=SQLite.retrieveData('accounts','email,username','',formDict['mail'])
		mailCompare=SQLite.retrieveData('accounts','email,username','',formDict['user'])
		if mailCompare == [] and userCompare==[]:
			try:
				newID=SQLite.getMaxValue('accountID','accounts')[0][0]+1
				SQLite.insertAccounts(newID,formDict['firstName'],formDict['lastName'],formDict['dateOfBirth'],formDict['user'],formDict['pass'],formDict['mail'],True,formDict['package'])
				accountData[formDict['user']]=classes.accounts(newID,formDict['firstName'],formDict['lastName'],formDict['dateOfBirth'],formDict['user'],formDict['pass'],formDict['mail'],True,formDict['package'])
			except:
				SQLite.insertAccounts(1,formDict['firstName'],formDict['lastName'],formDict['dateOfBirth'],formDict['user'],formDict['pass'],formDict['mail'],True,formDict['package'])
				accountData[formDict['user']]=classes.accounts(1,formDict['firstName'],formDict['lastName'],formDict['dateOfBirth'],formDict['user'],formDict['pass'],formDict['mail'],True,formDict['package'])
			sendResponse(self,302,'Location','/login.html',b'')
			userEmail= formDict['mail']
			contentSent="Dear "+formDict['firstName']+""",
This email is to confirm your account has been activated. 

Thank you""" 
			# send_message(sender, to, subject, content)
			Gmail.send_message('botbyali5@gmail.com', userEmail, 'Account Activation', contentSent)
			return accountData
		else:
			sendResponse(self,302,'Location','/newAccount.html',b'')

def login(self,decodedBody,allowLogin):
	decodedBody= re.sub('\%40','@',decodedBody)
	formList=re.split("&",decodedBody)
	pos=0
	for x in formList:
		formList[pos]=re.split("=", formList[pos])
		pos+=1
	output=SQLite.retrieveData('accounts','username,email,password',email=formList[0][1])

	try:
		#output[0][0] == username, output[0][1] == email output[0][2]==password
		#formList[0][1]== inputUser, formList[1][1]== inputPass
		if hashingPasswords.verify_password(output[0][2],formList[1][1]):
			allowLogin[output[0][0]]= [True,output[0][0]]
			body = output[0][0]
			return body, allowLogin
		else:
			sendResponse(self,200,'Content-Type','text/plain; utf-8',b'invalid username or password,else')
	except:

		sendResponse(self,200,'Content-Type','text/plain; utf-8',b'invalid username or password,except')

def createUser(self,formData,userData):
	formData=formData.split('&')
	createUserPos=0
	for element in range(len(formData)):
		formData[element]=formData[element].split('=')
	profileName=formData[0][1]
	restriction=formData[1][1]
	accountName=formData[2][1]
	accountID=SQLite.retrieveData('accounts','accountID',email=accountName)[0][0]
	maxUserID= SQLite.getMaxValueUsers('userID','users',accountID)[0][0]
	try:
		nothing=userData[profileName+str(accountID)]
		return userData
	except:
		pass
	if maxUserID is not None:
		SQLite.insertUsers(maxUserID+1,profileName,accountID,restriction)
		userData[profileName+str(accountID)]=classes.users(maxUserID+1,profileName,accountID,restriction)
	else:
		SQLite.insertUsers(1,profileName,accountID,restriction)
		userData[profileName+"1"]=classes.users(1,profileName,accountID,restriction)
	return userData
def getUsers(self, userData,accountName):
	userArr=[]
	accountID=SQLite.retrieveData('accounts','accountID',email=accountName)[0][0]
	for user in userData:
		if accountID == int(user[-1]):
			userArr.append(userData[user].profName)
	return userArr
def addToList(self,decodedBody,accountData,userData,showData):
	accId=str(accountData[decodedBody[1]].Id)
	userId=userData[decodedBody[2]+accId].userId
	showId=showData[decodedBody[0]].showId
	SQLite.addToList(showId,accId,userId)
	listData=SQLite.retrList()
	showCombo= SQLite.getMaxValue('showUserCombination','myList')[0][0]
	return listData,showCombo