from http.server import BaseHTTPRequestHandler
import os
from ftplib import FTP
import getpass
from urllib import parse, request
import re
from email.message import EmailMessage
import sys
import hash
from datetime import datetime
from bs4 import BeautifulSoup
global allowLogin
allowLogin=[False]
sys.path.append('database')
import SQLite
from dateFormat import checkDate, checkDateFormat
sys.path.append('C:/Users/alial/Desktop/Programs/Gmail API')
import Gmail
import classes
import socket


accountData = SQLite.retrAcc()
showData = SQLite.retrShow()
userData = SQLite.retrUsers()
listData = SQLite.retrList()


#print("Username:")
#user = input()
#password = getpass.getpass()

user="Ali" #ftp user name
password="aaj2005" #ftp password
ipaddress= socket.gethostbyname(socket.gethostname()) #ipv4 address

def sendResponse(self,responseCode,keyword,mime,data):
	self.send_response(responseCode)
	self.send_header(keyword, mime)
	self.end_headers()
	self.wfile.write(data)
def returnStoredFile(passedContent):
	global returnedFTPData
	returnedFTPData = passedContent

def insertShows(movieData):
	try:
		newID=SQLite.getMaxValue("showID", "tvShows")[0][0]+1
		if newID >= 1:
			SQLite.insertShows(newID,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction'])
			showData.append(classes.tvShows(newID,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction']))
	except:
			SQLite.insertShows(1,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction'])
			showData.append(classes.tvShows(1,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction']))

def updateShows(movieData,ID):
	try:
		if int(ID) >= 1:
			SQLite.updateShows(ID,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction'])
			global showData
			showData = SQLite.retrShow()
	except:
			SQLite.insertShows(1,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction'])
			showData.append(classes.tvShows(1,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction']))
def loadDropDown():
	maxID=SQLite.getMaxValue("showID", "tvShows")
	global listInStr
	listInStr = ""
	try:
		listInStr= maxID[0][0]
	except:
		listInStr="No Data Stored"
def openRequest(self,x,url):
	mimeType= os.path.splitext(x)
	dictionary={
		"html":"text/html",
		"js":"text/javascript"
	}
	self.send_response(200)
	self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
	self.end_headers()
	path = r"C:\Users\alial\Desktop\Programs\JavaScript Practice Programs\Movie Project\src"+ url + x
	with open(path,"r",encoding="utf-8") as f:
		self.wfile.write(f.read().encode("utf-8"))
def checkMovieData(self,movieDataInDict):
	if type(movieDataInDict) is dict:
		for x in movieDataInDict:
			if x=="name":
				movieNameLen=len(str(movieDataInDict[x]))
				if movieNameLen>150:
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


def creatNewAccount(self,decodedBody,invalidOption):
	for x in ('firstName','lastName','dateOfBirth','user','pass','mail','package'):
		arr = re.findall(x,decodedBody)
		if len(arr) > 1:
			if arr[0] != 'mail':
				invalidOption=False
				sendResponse(self,301,'Location','/newAccount.html',b'')
				break
			else:
				pass
		if arr ==[]:
			invalidOption=False
			sendResponse(self,301,'Location','/newAccount.html',b'')
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
					formDict[slotField]=hash.hash_password(decodedBody[slotNum[1]+1:formPos[pos][0]-1])
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
				accountData.append(classes.accounts(newID,formDict['firstName'],formDict['lastName'],formDict['dateOfBirth'],formDict['user'],formDict['pass'],formDict['mail'],True,formDict['package']))
			except:
				SQLite.insertAccounts(1,formDict['firstName'],formDict['lastName'],formDict['dateOfBirth'],formDict['user'],formDict['pass'],formDict['mail'],True,formDict['package'])
				accountData.append(classes.accounts(1,formDict['firstName'],formDict['lastName'],formDict['dateOfBirth'],formDict['user'],formDict['pass'],formDict['mail'],True,formDict['package']))
			sendResponse(self,301,'Location','/login.html',b'')
			userEmail= formDict['mail']
			contentSent="Dear "+formDict['firstName']+""",
This email is to confirm your account has been activated. 

Thank you""" 
			# send_message(sender, to, subject, content)
			Gmail.send_message('botbyali5@gmail.com', userEmail, 'Account Activation', contentSent)
		else:
			sendResponse(self,301,'Location','/newAccount.html',b'')




class GetHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		x =  parse.urlparse(self.path).path
		urlRecieved=parse.urlparse(self.path).path
		if(x in ("/addMovie.html", "/addMovie.js")):
			openRequest(self,x,r"\addMovie")
		elif urlRecieved in ("/newUser.html","/newUser.js"):
			if allowLogin[0] and self.address_string() == allowLogin[2]:
				openRequest(self,x,r"\createUser")
			else:
				sendResponse(self,301,'Location','/login.html',b'')
		elif urlRecieved in ("/newAccount.html","/newAccount.js"):
			openRequest(self,x,r"\createAccount")
		elif urlRecieved in ("/newUser.html","/newUser.js"):
			openRequest(self,x,r"\createUser")
		elif urlRecieved in ("/login.html","/Login.js"):
			openRequest(self,x,r"\login")
		elif urlRecieved == "/getArrayCount":
			loadDropDown()
			sendResponse(self,200,'Content-Type','text/strings; utf-8',str(listInStr).encode("utf-8"))
		elif urlRecieved == "/loadImg":
			fh = request.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Poster/'+decodedBody+'.jpg')
			sendResponse(self,200,'Content-Type','image/jpeg; utf-8',fh.read())
		elif urlRecieved == "/loadVid":
			fh = request.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Video/'+decodedBody+'.mp4')
			sendResponse(self,200,'Content-Type','video/mp4; utf-8',fh.read())
		elif urlRecieved =="/getAccName":
			sendResponse(self,200,'Content-Type','text/plain; utf-8',allowLogin[1].encode('utf-8'))
		else:
			sendResponse(self,200,'Content-Type','application/json; utf-8',b'')

	def do_POST(self):
		if self.request.getsockname()[0] == ipaddress:
			urlRecieved=parse.urlparse(self.path).path
			content_length = int(self.headers.get('content-length'))
			body = self.rfile.read(content_length)
			global decodedBody
			decodedBody = body.decode("utf-8")
			global ftp
			ftp = FTP(ipaddress)
			ftp.login(user,password)
			if  decodedBody == 'loadDropDown':
				loadDropDown()
				sendResponse(self,200,'Content-Type','text/strings; utf-8',str(listInStr).encode("utf-8"))
			elif urlRecieved == "/getName":
				if decodedBody !="":
					showInfo=SQLite.retrieveData('tvShows',"*",decodedBody)
					showInfo=re.sub('[()]','',str(showInfo))
					showInfo=re.sub("[\'']",'',showInfo)
					showInfo= showInfo[1:-1]
					sendResponse(self,200,'Content-Type','application/json; utf-8',str(showInfo).encode('utf-8'))
				else:
					sendResponse(self,200,'Content-Type','application/json; utf-8',b'None')
			
			elif urlRecieved == "/send":
				condition=False
				movieDataInDict=eval(decodedBody)
				condition = checkMovieData(self,movieDataInDict)
				if condition:
						insertShows(movieDataInDict)
						sendResponse(self,200,'Content-Type','text/plain; utf-8',b'True')
			elif urlRecieved == "/update":
				condition=False
				movieDataInDict=eval(decodedBody)
				returnedValues = checkMovieData(self,movieDataInDict)
				condition = returnedValues[0]
				movieID = returnedValues[1]
				if condition:
						updateShows(movieDataInDict,movieID)
						sendResponse(self,200,'Content-Type','text/plain; utf-8',b'True')
				else:
						sendResponse(self,200,'Content-Type','text/plain; utf-8',b'False')
			elif urlRecieved == "/loadImg":
				ftp = FTP(ipaddress)
				ftp.login(user,password)
				fh = request.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Poster/'+decodedBody+'.jpg')
				sendResponse(self,200,'Content-Type','image/jpeg; utf-8',fh.read())
			elif urlRecieved == "/loadVid":
				ftp = FTP(ipaddress)
				ftp.login(user,password)
				fh = request.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Video/'+decodedBody+'.mp4')
				sendResponse(self,200,'Content-Type','video/mp4; utf-8',fh.read())
			elif urlRecieved == "/login":
				decodedBody= re.sub('\%40','@',decodedBody)
				formList=re.split("&",decodedBody)
				pos=0
				ftp.cwd('User Data')
				for x in formList:
					formList[pos]=re.split("=", formList[pos])
					pos+=1
				output=SQLite.retrieveData('accounts','username,email,password','',formList[0][1])

				try:
					#output[0][0] == username, output[0][1] == email output[0][2]==password
					#formList[0][1]== inputUser, formList[1][1]== inputPass
					if hash.verify_password(output[0][2],formList[1][1]):
						global allowLogin
						allowLogin=True, output[0][0], self.address_string()
						sendResponse(self,301,'Location','/newUser.html',b'')
					else:
						sendResponse(self,200,'Content-Type','text/plain; utf-8',b'invalid username or password,else')
				except:
					sendResponse(self,200,'Content-Type','text/plain; utf-8',b'invalid username or password,else')
			elif urlRecieved == "/createAccount":
				invalidOption=True
				decodedBody= re.sub('\%40','@',decodedBody)
				creatNewAccount(self,decodedBody,invalidOption)


if __name__ == '__main__':
	from http.server import HTTPServer
	server= HTTPServer((ipaddress,1234), GetHandler)
	print("Server Starting")
	server.serve_forever()
