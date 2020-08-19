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





class GetHandler(BaseHTTPRequestHandler):
	global allowLogin
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
		if(x in ("/addMovie.html", "/addMovie.js")):
			openRequest(self,x,r"\addMovie")

		elif urlRecieved in ("/newUser.html","/newUser.js"):
			try:
				if acceptLogin[username][0]:
					openRequest(self,x,r'\createUser')
				else:
					sendResponse(self,301,'Location','/login.html',b'')
			except:
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
			fh = ftpRequest.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Poster/'+decodedBody+'.jpg')
			sendResponse(self,200,'Content-Type','image/jpeg; utf-8',fh.read())
		elif urlRecieved == "/loadVid":
			fh = ftpRequest.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Video/'+decodedBody+'.mp4')
			sendResponse(self,200,'Content-Type','video/mp4; utf-8',fh.read())
		elif urlRecieved =="/getAccName":
			sendResponse(self,200,'Content-Type','text/plain; utf-8',acceptLogin[username][1].encode('utf-8'))
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
						self.showData=insertShows(movieDataInDict,self.showData)
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
				returnedData=login(self,decodedBody,allowLogin)
				if returnedData is not None:
					global username
					username=returnedData[0]
					global acceptLogin
					acceptLogin=returnedData[1]
				sendResponse(self,301,'Location','/newUser.html',b'')
			elif urlRecieved == "/createAccount":
				invalidOption=True
				decodedBody= re.sub('\%40','@',decodedBody)
				accountDataUpdated=createNewAccount(self,decodedBody,invalidOption,self.accountData)
				accountData=accountDataUpdated
			elif urlRecieved == "/createUser":
				self.userData=createUser(self,decodedBody,self.userData)
				sendResponse(self,301,'Location','/newUser.html',b'')
			elif urlRecieved == "/getUsers":
				userArr=getUsers(self,self.userData,decodedBody)
				userList= ""
				for name in userArr:
					userList= userList +','+name
				userList=userList[1:]
				sendResponse(self,200,'Content-Type','text/plain',userList.encode('utf-8'))

if __name__ == '__main__':
	from http.server import HTTPServer
	server= HTTPServer((ipaddress,1234), GetHandler)
	print("Server Starting")
	server.serve_forever()