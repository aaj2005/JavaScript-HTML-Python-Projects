from http.server import BaseHTTPRequestHandler
import json
import io
import cgi
import os
from ftplib import FTP
import getpass
from urllib import parse 
from urllib import request 
import re
from ast import literal_eval
import smtplib
from email.message import EmailMessage
import sys
JSONFileName=0
sys.path.insert(1, 'Gmail API Path')
import Gmail

#print("Username:")
#user = input()
#password = getpass.getpass()

user="username" #ftp user name
password="password" #ftp password
ipaddress='yourIP' #ipv4 address

def returnStoredFile(passedContent):
	global returnedFTPData
	returnedFTPData = passedContent
def getJSON(listInput):
	b=0   
	newList=[]
	for p in listInput:
		if p[1]==".json":
			newList.append(p[0])
		b+=1
	return newList
def updateData(newData,filename):
	ftp.cwd('JSON Files')
	ioFile=io.BytesIO(newData)
	ftp.storbinary('Stor '+str(filename)+".json", ioFile)
def loadDropDown():
			ftp = FTP(ipaddress)
			ftp.login(user,password)
			ftp.cwd('JSON Files')
			storedFiles=[]
			z=0
			for x in ftp.nlst():
				storedFiles.append(x)
				storedFiles[z]=os.path.splitext(storedFiles[z])
				z+=1
			updatedList=getJSON(storedFiles)
			global listInStr
			listInStr = ""
			z=0
			for x in updatedList:
				
				listInStr += x +","
				updatedList[z]=int(updatedList[z])
				z+=1
			listInStr = listInStr[:-1]	
			try:
				JSONFileName = max(updatedList)

			except:
				null=""
			return JSONFileName	

class GetHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		urlRecieved=parse.urlparse(self.path).path
		x =  parse.urlparse(self.path).path
		dictionary={
			"html":"text/html",
			"js":"text/javascript"
		}
		if(x in ("/JSON-Object.html", "/JSON-Object.js")):
			self.send_response(200)
			mimeType= os.path.splitext(x)
			self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
			self.end_headers()
			path = r"C:\Users\alial\OneDrive\Desktop\Programs\JavaScript Practice Programs\Movie Project" + x
			with open(path,"r",encoding="utf-8") as f:
				self.wfile.write(f.read().encode("utf-8"))
		elif (x in ("/searchMenu.html","/searchMenu.js")):
			self.send_response(200)
			mimeType= os.path.splitext(x)
			self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
			self.end_headers()
			path = r"C:\Users\alial\OneDrive\Desktop\Programs\JavaScript Practice Programs\Movie Project" + x
			with open(path,"r",encoding="utf-8") as f:
				self.wfile.write(f.read().encode("utf-8"))
		elif (x in ("/newUser.html","/newUser.js")):
			self.send_response(200)
			mimeType= os.path.splitext(x)
			self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
			self.end_headers()
			path = r"C:\Users\alial\OneDrive\Desktop\Programs\JavaScript Practice Programs\Movie Project" + x
			with open(path,"r",encoding="utf-8") as f:
				self.wfile.write(f.read().encode("utf-8"))
		elif (x in ("/login.html","/Login.js")):
			self.send_response(200)
			mimeType= os.path.splitext(x)
			self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
			self.end_headers()
			path = r"C:\Users\alial\OneDrive\Desktop\Programs\JavaScript Practice Programs\Movie Project" + x
			with open(path,"r",encoding="utf-8") as f:
				self.wfile.write(f.read().encode("utf-8"))
		elif urlRecieved == "/getArrayCount":
			JSONFileName=loadDropDown()
			self.send_response(200)
			self.send_header('Content-Type', 'text/strings; utf-8')
			self.end_headers()
			self.wfile.write(str(JSONFileName).encode("utf-8"))
		elif urlRecieved == "/loadImg":
			fh = request.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Poster/'+decodedBody+'.jpg')
			self.send_response(200)
			self.send_header('Content-Type', 'image/jpeg; utf-8')
			self.end_headers()
			self.wfile.write(fh.read())
		elif urlRecieved == "/loadVid":
			fh = request.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Video/'+decodedBody+'.mp4')
			self.send_response(200)
			self.send_header('Content-Type', 'video/mp4; utf-8')
			self.end_headers()
			self.wfile.write(fh.read())
		else:
			self.send_response(200)
			self.send_header('Content-Type', 'application/json; utf-8')
			self.end_headers()
			self.wfile.write(b"")



	def do_POST(self):
		urlRecieved=parse.urlparse(self.path).path
		global JSONFileName
		content_length = int(self.headers.get('content-length'))
		body = self.rfile.read(content_length)
		global decodedBody
		decodedBody = body.decode("utf-8")
		global ftp
		ftp = FTP(ipaddress)
		ftp.login(user,password)
		if  decodedBody == 'loadDropDown':
			loadDropDown()
			self.send_response(200)
			self.send_header('Content-Type', 'text/strings; utf-8')
			self.end_headers()
			self.wfile.write(listInStr.encode("utf-8"))
		elif urlRecieved == "/getName":
			ftp = FTP(ipaddress)
			ftp.login(user,password)
			ftp.cwd('JSON Files')
			ftp.retrbinary('RETR '+decodedBody+".json",returnStoredFile)
			self.send_response(200)
			self.send_header('Content-Type', 'application/json; utf-8')
			self.end_headers()
			self.wfile.write(returnedFTPData)
		
		elif urlRecieved == "/send":
			
			updateData(body,int(JSONFileName)+1)
			self.send_response(200)
			self.send_header('Content-Type', 'text/javascript; utf-8')
			self.end_headers()
			JSONFileName+=1
		elif urlRecieved == "/loadImg":
			ftp = FTP(ipaddress)
			ftp.login(user,password)
			fh = request.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Poster/'+decodedBody+'.jpg')
			self.send_response(200)
			self.send_header('Content-Type', 'image/jpeg; utf-8')
			self.end_headers()
			self.wfile.write(fh.read())
		elif urlRecieved == "/loadVid":
			ftp = FTP(ipaddress)
			ftp.login(user,password)
			fh = request.urlopen('ftp://'+user+":"+password+'@'+ipaddress+'/Movie Video/'+decodedBody+'.mp4')
			self.send_response(200)
			self.send_header('Content-Type', 'video/mp4; utf-8')
			self.end_headers()
			self.wfile.write(fh.read())
		elif urlRecieved == "/login":
			ftp = FTP(ipaddress)
			ftp.login(user,password)
			

			formList=re.split("&",decodedBody)
			pos=0
			ftp.cwd('User Data')
			for x in formList:
				formList[pos]=re.split("=", formList[pos])
				pos+=1
			try:
				self.send_response(200)
				self.end_headers()
				ftp.retrbinary('RETR '+formList[0][1]+".json",returnStoredFile)
				decodedFTPData=returnedFTPData.decode('utf-8')
				decodedFTPData=literal_eval(decodedFTPData)
				if decodedFTPData['pass']==formList[1][1]:
					self.wfile.write(b'login successful')
				else:
					self.wfile.write(b'invalid username or password,else')
			except:
				self.wfile.write(b'invalid username or password, error')
		elif urlRecieved == "/createUser":
			ftp = FTP(ipaddress)
			ftp.login(user,password)
			decodedBody= re.sub('\%40','@',decodedBody)
			formList=re.split("&",decodedBody)
			print("formList",formList)
			pos=0
			formDict={}

			for x in formList:
				formList[pos]=re.split("=", formList[pos])
				formDict[formList[pos][0]]=formList[pos][1]
				pos+=1
			ftp.cwd('User Data')
			try:
				ftp.retrlines('Retr '+formDict['user']+'.json')
				self.send_response(301)
				self.send_header('Location','/newUser.html')
				errorTrueFalse= True
			except:
				ioFile=io.BytesIO(json.dumps(formDict).encode('utf-8'))
				ftp.storbinary('Stor '+formDict['user']+'.json', ioFile)
				errorTrueFalse=False
				userEmail= formDict['mail']
				print(formDict)
				contentSent="Dear "+formDict['user']+""",
This email is to confirm your account has been activated. 

Thank you""" 
				#send_message(sender, to, subject, content):
				Gmail.send_message('botbyali5@gmail.com', userEmail, 'Account Activation', contentSent)
				self.send_response(301)
				self.send_header('Location','/login.html')
				print("check")
				self.end_headers()

			if errorTrueFalse:
				print("username already exists")
				self.send_response(301)
				self.send_header('Location','/newUser.html')
				self.end_headers()
			
if __name__ == '__main__':
	from http.server import HTTPServer
	server= HTTPServer((ipaddress,1234), GetHandler)
	print("Server Starting")
	server.serve_forever()

