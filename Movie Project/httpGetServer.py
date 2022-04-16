from http.server import BaseHTTPRequestHandler
from ftplib import FTP
from urllib import parse
from urllib import  request as ftpRequest
import re
import sys
import socket
from post import *
from get import *
sys.path.append('database')
import SQLite

import classes



user="Ali" #ftp user name
password="aaj2005" #ftp password
ipaddress= socket.gethostbyname(socket.gethostname()) #ipv4 address
global username


class GetHandler(BaseHTTPRequestHandler):
	username=""
	allowLogin={}
	accountData = SQLite.retrAcc()
	showData = SQLite.retrShow()
	userData = SQLite.retrUsers()
	listData = SQLite.retrList()
	for accountClass in accountData:
		allowLogin[accountClass]=[False,'']
	def do_GET(self):
		x =  parse.urlparse(self.path).path
		urlRecieved=parse.urlparse(self.path).path
		if x in ("/addMovie.html", "/addMovie.js"):
			openRequest(self,x,r"\addMovie")

		elif urlRecieved in ("/newUser.html","/newUser.js"):
			try:
				if GetHandler.allowLogin[GetHandler.username][0]:
					openRequest(self,x,r'\createUser')
					return
			except:
				sendResponse(self,302,'Location','/login.html',b'')
		elif urlRecieved in ('/searchMenu.html','/searchMenu.js'):
			try:
				
				if GetHandler.allowLogin[GetHandler.username][0]:
					openRequest(self,x,r'\searchMovie')
				else:
					sendResponse(self,302,'Location','/login.html',b'')
			except:
				sendResponse(self,302,'Location','/login.html',b'')
		elif urlRecieved in ("/newAccount.html","/newAccount.js"):
			openRequest(self,x,r"\createAccount")
		elif urlRecieved in ("/login.html","/Login.js"):
			openLoginPage=True
			for accounts in GetHandler.allowLogin:
				if GetHandler.allowLogin[accounts][0]== True:
					GetHandler.username=accounts
					openLoginPage=False
					sendResponse(self,302,'Location','/newUser.html',b'')
			if openLoginPage:
				openRequest(self,x,r"\login")
		elif urlRecieved == "/getArrayCount":
			listInStr=loadDropDown()
			sendResponse(self,200,'Content-Type','text/strings; utf-8',str(listInStr).encode("utf-8"))
		elif urlRecieved == "/loadImg":
			fh = ftpRequest.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Poster/'+decodedBody+'.jpg')
			sendResponse(self,200,'Content-Type','image/jpeg; utf-8',fh.read())
		elif urlRecieved == "/loadVid":
			fh = ftpRequest.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Video/'+decodedBody+'.mp4')
			sendResponse(self,200,'Content-Type','video/mp4; utf-8',fh.read())
		elif urlRecieved =="/getAccName":
			sendResponse(self,200,'Content-Type','text/plain; utf-8',GetHandler.allowLogin[GetHandler.username][1].encode('utf-8'))
		elif urlRecieved == '/getProfName':
			sendResponse(self,200,'Content-Type','text/plain; utf-8',profname.encode('utf-8'))
		elif urlRecieved =='/getMovieName':
			showListWithId=''
			for showName in GetHandler.showData:
				showListWithId+=','+showName+':'+str(GetHandler.showData[showName].showId)
			showListWithId= showListWithId[1:]
			sendResponse(self,200,'Content-Type','text/plain; utf-8',showListWithId.encode('utf-8'))
		elif urlRecieved == '/logout':
			for accounts in GetHandler.allowLogin:
				if GetHandler.allowLogin[accounts][0] == True:
					GetHandler.allowLogin[accounts][0]=False
			sendResponse(self,200,'Location','/login.html',b'')
		elif urlRecieved =='/styles.css':
			openRequest(self,x,'')
		elif urlRecieved =='/login.css':
			openRequest(self,x,r'\login')
		elif urlRecieved =='/accountStyles.css':
			openRequest(self,x,r'\createAccount')
		elif urlRecieved =='/newUser.css':
			openRequest(self,x,r'\createUser')
		elif urlRecieved == '/loginImage.jpg':
			ftp = FTP(ipaddress)
			ftp.login(user,password)
			fh = ftpRequest.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Images/loginImage2.jpg')
			sendResponse(self,200,'Content-Type','image/jpg; utf-8',fh.read())
		elif urlRecieved == '/favicon.ico':
			ftp = FTP(ipaddress)
			ftp.login(user,password)
			fh = ftpRequest.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Images/icon.ico')
			sendResponse(self,200, 'Content-Type','image/x-icon; utf-8',fh.read())
		else:
			sendResponse(self,200,'Content-Type','application/json; utf-8',b'')
			
	def do_POST(self):
		if self.request.getsockname()[0] == ipaddress:
			urlRecieved=parse.urlparse(self.path).path
			content_length = int(self.headers.get('content-length'))
			receivedFormData = self.rfile.read(content_length)
			global decodedBody
			decodedBody = receivedFormData.decode("utf-8")
			global ftp
			ftp = FTP(ipaddress)
			ftp.login(user,password)
			if  decodedBody == 'loadDropDown':
				listInStr=loadDropDown()
				sendResponse(self,200,'Content-Type','text/strings; utf-8',str(listInStr).encode("utf-8"))
			elif urlRecieved == "/getShowData":
				if decodedBody !="":
					showInfo=SQLite.retrieveData('tvShows',"*",showId=decodedBody)
					showInfo=re.sub('[()]','',str(showInfo))
					showInfo=re.sub("[\'']",'',showInfo)
					showInfo= showInfo[1:-1]
					sendResponse(self,200,'Content-Type','application/json; utf-8',str(showInfo).encode('utf-8'))
				else:
					sendResponse(self,200,'Content-Type','application/json; utf-8',b'None')
			
			elif urlRecieved == "/send":

				movieDataInDict=eval(decodedBody)
				condition = checkMovieData(self,movieDataInDict)
				if condition:
						GetHandler.showData=insertShows(movieDataInDict,GetHandler.showData)
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
				fh = ftpRequest.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Poster/'+decodedBody+'.jpg')
				sendResponse(self,200,'Content-Type','image/jpeg; utf-8',fh.read())
			elif urlRecieved == "/login":
				returnedData=login(self,decodedBody,GetHandler.allowLogin)
				if returnedData is not None:
					GetHandler.username=returnedData[0]
					GetHandler.allowLogin=returnedData[1]
				sendResponse(self,302,'Location','/newUser.html',b'')
			elif urlRecieved == "/createAccount":
				invalidOption=True
				decodedBody= re.sub('\%40','@',decodedBody)
				accountDataUpdated=createNewAccount(self,decodedBody,invalidOption,GetHandler.accountData)
				accountData=accountDataUpdated
			elif urlRecieved == "/createUser":
				GetHandler.userData=createUser(self,decodedBody,GetHandler.userData)
				sendResponse(self,302,'Location','/newUser.html',b'')
			elif urlRecieved == "/getUsers":
				userArr=getUsers(self,GetHandler.userData,decodedBody)
				userList= ""
				for name in userArr:
					userList= userList +','+name
				userList=userList[1:]
				sendResponse(self,200,'Content-Type','text/plain',userList.encode('utf-8'))
			elif urlRecieved == '/searchMenu':
				global profname
				profname= decodedBody
				sendResponse(self,200,'Content-Type','text/plain',b'')
			elif urlRecieved == '/addToList':
				decodedBody=eval(decodedBody)
				showId=GetHandler.showData[decodedBody[0]].showId
				accountId= GetHandler.accountData[decodedBody[1]].Id
				userId= GetHandler.userData[decodedBody[2]+str(accountId)].userId
				showName=SQLite.retrieveData('tvShows','name',showId=showId)[0][0]
				try:
					GetHandler.listData[decodedBody[1]+':'+decodedBody[2]+':'+str(showId)]
					SQLite.removeShowFromList(showId,str(accountId)+':'+str(userId))
					GetHandler.listData=SQLite.retrList()
					sendResponse(self,200,'Content-Type','text/plain',showName.encode('utf-8'))
				except KeyError as e:
					returnedListData=addToList(self,decodedBody,GetHandler.accountData,GetHandler.userData,GetHandler.showData)
					GetHandler.listData=returnedListData[0]
					showCombo=returnedListData[1]
					sendResponse(self,200,'Content-Type','text/plain',GetHandler.showData[decodedBody[0]].name.encode('utf-8'))
			elif urlRecieved =='/getList':
				decodedBody=decodedBody.split(',')
				accountName=decodedBody[0]
				profileName=decodedBody[1]
				showList=''
				for accountUserID in GetHandler.listData:
					accountUserIDSplit=accountUserID.split(':')
					if accountName == accountUserIDSplit[0] and profileName == accountUserIDSplit[1]:
						showId=GetHandler.listData[accountUserID].showId
						showName=SQLite.retrieveData('tvShows','name',showId=showId)[0][0]
						showList += ','+showName
				showList=showList[1:]
				sendResponse(self,200,'Content-Type','text/plain; utf-8',showList.encode('utf-8'))
if __name__ == '__main__':
	from http.server import HTTPServer
	server= HTTPServer((ipaddress,1234), GetHandler)
	print("Server Starting at ",ipaddress)
	server.serve_forever()