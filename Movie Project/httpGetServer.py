from http.server import BaseHTTPRequestHandler
import json
import os
from ftplib import FTP
import getpass
from urllib import parse, request
import re
from email.message import EmailMessage
import sys
import hash
from datetime import datetime
global allowLogin
allowLogin=False
sys.path.append('database')
import SQLite
from dateFormat import checkDate, checkDateFormat
sys.path.append('C:/Users/alial/Desktop/Programs/Gmail API')
import Gmail
#print("Username:")
#user = input()
#password = getpass.getpass()

user="Ali" #ftp user name
password="aaj2005" #ftp password
ipaddress='192.168.100.40' #ipv4 address


def returnStoredFile(passedContent):
	global returnedFTPData
	returnedFTPData = passedContent

def insertShows(movieData):
	try:
		newID=SQLite.getMaxValue("showID", "tvShows")[0][0]+1
		if newID >= 1:
			SQLite.insertShows(newID,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction'])
	except:
			SQLite.insertShows(1,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction'])
def updateShows(movieData,ID):
	try:
		if int(ID) >= 1:
			SQLite.updateShows(ID,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction'])
	except:
			SQLite.insertShows(1,movieData['name'],movieData['date'],movieData['category'],movieData['runTime'],movieData['expiry'],movieData['restriction'])
def loadDropDown():
			maxID=SQLite.getMaxValue("showID", "tvShows")
			global listInStr
			listInStr = ""
			try:
				listInStr= maxID[0][0]
			except:
				listInStr="No Data Stored"
class GetHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		urlRecieved=parse.urlparse(self.path).path
		x =  parse.urlparse(self.path).path
		dictionary={
			"html":"text/html",
			"js":"text/javascript"
		}
		if(x in ("/addMovie.html", "/addMovie.js")):
			self.send_response(200)
			mimeType= os.path.splitext(x)
			self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
			self.end_headers()
			path = r"C:\Users\alial\Desktop\Programs\JavaScript Practice Programs\Movie Project\src\addMovie" + x
			with open(path,"r",encoding="utf-8") as f:
				self.wfile.write(f.read().encode("utf-8"))
		elif (x in ("/searchMenu.html","/searchMenu.js")):
			if allowLogin:
				self.send_response(200)
				mimeType= os.path.splitext(x)
				self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
				self.end_headers()
				path = r"C:\Users\alial\Desktop\Programs\JavaScript Practice Programs\Movie Project\src\searchMovie" + x
				with open(path,"r",encoding="utf-8") as f:
					self.wfile.write(f.read().encode("utf-8"))
			else:
				self.send_response(301)
				self.send_header('Location','/login.html')
				self.end_headers()
		elif (x in ("/newAccount.html","/newAccount.js")):
			self.send_response(200)
			mimeType= os.path.splitext(x)
			self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
			self.end_headers()
			path = r"C:\Users\alial\Desktop\Programs\JavaScript Practice Programs\Movie Project\src\createAccount" + x
			with open(path,"r",encoding="utf-8") as f:
				self.wfile.write(f.read().encode("utf-8"))
		elif (x in ("/newUser.html","/newUser.js")):
			self.send_response(200)
			mimeType= os.path.splitext(x)
			self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
			self.end_headers()
			path = r"C:\Users\alial\Desktop\Programs\JavaScript Practice Programs\Movie Project\src\createUser" + x
			with open(path,"r",encoding="utf-8") as f:
				self.wfile.write(f.read().encode("utf-8"))	
		elif (x in ("/login.html","/Login.js")):
			self.send_response(200)
			mimeType= os.path.splitext(x)
			self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
			self.end_headers()
			path = r"C:\Users\alial\Desktop\Programs\JavaScript Practice Programs\Movie Project\src\login" + x
			with open(path,"r",encoding="utf-8") as f:
				self.wfile.write(f.read().encode("utf-8"))
		elif urlRecieved == "/getArrayCount":
			loadDropDown()
			self.send_response(200)
			self.send_header('Content-Type', 'text/strings; utf-8')
			self.end_headers()
			self.wfile.write(str(listInStr).encode("utf-8"))
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
		print(self.request.getsockname())
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
			self.send_response(200)
			self.send_header('Content-Type', 'text/strings; utf-8')
			self.end_headers()
			self.wfile.write(str(listInStr).encode("utf-8"))
		elif urlRecieved == "/getName":
			if decodedBody !="":
				showData=SQLite.retrieveData('tvShows',"*",decodedBody)
				showData=re.sub('[()]','',str(showData))
				showData=re.sub("[\'']",'',showData)
				showData= showData[1:-1]
				self.send_response(200)
				self.send_header('Content-Type', 'application/json; utf-8')
				self.end_headers()
				self.wfile.write(str(showData).encode('utf-8'))
			else:
				self.send_response(200)
				self.send_header('Content-Type', 'application/json; utf-8')
				self.end_headers()
				self.wfile.write(b'None')
		
		elif urlRecieved == "/send":
			condition=False
			movieDataInDict=eval(decodedBody)
			if type(movieDataInDict) is dict:
				for x in movieDataInDict:
					if x=="name":
						movieNameLen=len(movieDataInDict[x])
						if movieNameLen>150:
							self.send_response(200)
							self.send_header('Content-Type','text/plain')
							self.end_headers()
							self.wfile.write(str(result).encode('utf-8'))
							break
						else:
							pass
					elif x=="date":
						result=checkDateFormat(movieDataInDict,x,False)
						if result:
							checkDate(movieDataInDict,x)
						else:
							self.send_response(200)
							self.send_header('Content-Type','text/plain')
							self.end_headers()
							self.wfile.write(str(result).encode('utf-8'))
							break
					elif x=="category":
						categoryLen=len(movieDataInDict[x])
						if categoryLen>150:
							self.send_response(200)
							self.send_header('Content-Type','text/plain')
							self.end_headers()
							self.wfile.write(str(result).encode('utf-8'))
							break
						else:
							pass
					elif x=="runTime":
						try:
							int(movieDataInDict[x])
						except:
							self.send_response(200)
							self.send_header('Content-Type','text/plain')
							self.end_headers()
							self.wfile.write(str(result).encode('utf-8'))
							break
					elif x=="expiry":
						result=checkDateFormat(movieDataInDict,x,True)
						if result:
							checkDate(movieDataInDict,x)
						else:
							self.send_response(200)
							self.send_header('Content-Type','text/plain')
							self.end_headers()
							self.wfile.write(str(result).encode('utf-8'))
							break
					elif x=="restriction":
						try:
							int(movieDataInDict[x]) 
							condition = True
						except:
							self.send_response(200)
							self.send_header('Content-Type','text/plain')
							self.end_headers()
							self.wfile.write(str(result).encode('utf-8'))
							break
					else:
						condition=False
						break
			else:
				self.send_response(200)
				self.send_header('Content-Type','text/plain')
				self.end_headers()
				self.wfile.write(b'False')
			if condition:
					insertShows(movieDataInDict)
					self.send_response(200)
					self.send_header('Content-Type','text/plain')
					self.end_headers()
					self.wfile.write(b'True')
		elif urlRecieved == "/update":
			condition=False
			movieDataInDict=eval(decodedBody)
			print(decodedBody)
			if type(movieDataInDict) is dict:
				for x in movieDataInDict:
					if x=="name":
						movieNameLen=len(movieDataInDict[x])
						if movieNameLen>150:
							self.send_response(200)
							self.send_header('Content-Type','text/plain')
							self.end_headers()
							self.wfile.write(str(result).encode('utf-8'))
							break
						else:
							pass
					elif x=="date":
						result=checkDateFormat(movieDataInDict,x,False)
						if result:
							checkDate(movieDataInDict,x)
						else:
							self.send_response(200)
							self.send_header('Content-Type','text/plain')
							self.end_headers()
							self.wfile.write(str(result).encode('utf-8'))
							break
					elif x=="category":
						categoryLen=len(movieDataInDict[x])
						if categoryLen>150:
							self.send_response(200)
							self.send_header('Content-Type','text/plain')
							self.end_headers()
							self.wfile.write(str(result).encode('utf-8'))
							break
						else:
							pass
					elif x=="runTime":
						try:
							int(movieDataInDict[x])
						except:
							self.send_response(200)
							self.send_header('Content-Type','text/plain')
							self.end_headers()
							self.wfile.write(str(result).encode('utf-8'))
							break
					elif x=="expiry":
						result=checkDateFormat(movieDataInDict,x,True)
						if result:
							checkDate(movieDataInDict,x)
						else:
							self.send_response(200)
							self.send_header('Content-Type','text/plain')
							self.end_headers()
							self.wfile.write(str(result).encode('utf-8'))
							break
					elif x=="restriction":
						try:
							int(movieDataInDict[x]) 
							condition = True
						except:
							self.send_response(200)
							self.send_header('Content-Type','text/plain')
							self.end_headers()
							self.wfile.write(str(result).encode('utf-8'))
							break
					elif x=="id":
						movieID= movieDataInDict[x]
					else:
						condition=False
						break
			else:
				self.send_response(200)
				self.send_header('Content-Type','text/plain')
				self.end_headers()
				self.wfile.write(b'False')
			if condition:
					updateShows(movieDataInDict,movieID)
					self.send_response(200)
					self.send_header('Content-Type','text/plain')
					self.end_headers()
					self.wfile.write(b'True')
			else:
					self.send_response(200)
					self.send_header('Content-Type','text/plain')
					self.end_headers()
					self.wfile.write(b'False')
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
			decodedBody= re.sub('\%40','@',decodedBody)
			formList=re.split("&",decodedBody)
			pos=0
			ftp.cwd('User Data')
			for x in formList:
				formList[pos]=re.split("=", formList[pos])
				pos+=1
			output=SQLite.retrieveData('accounts','username,email,password','',formList[0][1])
			try:
				if hash.verify_password(output[0][2],formList[1][1]):
					global allowLogin
					allowLogin=True
					self.send_response(301)
					self.send_header('Location','/searchMenu.html')
					self.end_headers()
				else:
					self.send_response(200)
					self.end_headers()
					self.wfile.write(b'invalid username or password,else')
			except:
				self.send_response(200)
				self.end_headers()
				self.wfile.write(b'invalid username or password,else')
		elif urlRecieved == "/createAccount":
			invalidOption=True
			decodedBody= re.sub('\%40','@',decodedBody)
			print(decodedBody)
			for x in ('firstName','lastName','dateOfBirth','user','pass','mail','package'):
				arr = re.findall(x,decodedBody)
				print(arr)
				if len(arr) > 1:
					if arr[0] != 'mail':
						invalidOption=False
						self.send_response(301)
						self.send_header('Location','/newAccount.html')
						self.end_headers()
						break
					else:
						pass
				if arr ==[]:
					invalidOption=False
					self.send_response(301)
					self.send_header('Location','/newAccount.html')
					self.end_headers()
					break
			if invalidOption:
				formPos=[]
				pos=0
				for x in ('firstName','lastName','dateOfBirth','user','pass','mail','package'):
					formPos.append(re.search(x,decodedBody))
					formPos[pos]=formPos[pos].span()
					pos+=1
				print(formPos)
				formDict={}
				pos=1
				for x in formPos:
					if x[1]!= formPos[-1][1]:
						if decodedBody[x[0]:x[1]] =='pass':
							print([x[0],x[1]],x[1]+1,formPos[2][0]-1)
							formDict[decodedBody[x[0]:x[1]]]=hash.hash_password(decodedBody[x[1]+1:formPos[pos][0]-1])
						else:
							print([x[0],x[1]],x[1]+1,formPos[2][0]-1)
							formDict[decodedBody[x[0]:x[1]]]=decodedBody[x[1]+1:formPos[pos][0]-1]
					else:
						formDict[decodedBody[x[0]:x[1]]]=decodedBody[x[1]+1:]
					pos+=1
				for x in formDict:
					print(x)
					formDict[x]=re.sub('\+',' ',formDict[x])
				
				userCompare=SQLite.retrieveData('accounts','email,username','',formDict['mail'])
				mailCompare=SQLite.retrieveData('accounts','email,username','',formDict['user'])
				if mailCompare == [] and userCompare==[]:
					try:
						newID=SQLite.getMaxValue('accountID','accounts')[0][0]+1
						SQLite.insertAccounts(newID,formDict['firstName'],formDict['lastName'],formDict['dateOfBirth'],formDict['user'],formDict['pass'],formDict['mail'],True,formDict['package'])
					except:
						SQLite.insertAccounts(1,formDict['firstName'],formDict['lastName'],formDict['dateOfBirth'],formDict['user'],formDict['pass'],formDict['mail'],True,formDict['package'])
					self.send_response(301)
					self.send_header('Location','/login.html')
					self.end_headers()
					userEmail= formDict['mail']
					contentSent="Dear "+formDict['firstName']+""",
This email is to confirm your account has been activated. 

Thank you""" 
					# send_message(sender, to, subject, content)
					Gmail.send_message('botbyali5@gmail.com', userEmail, 'Account Activation', contentSent)
				else:
					self.send_response(301)
					self.send_header('Location','/newAccount.html')
					self.end_headers()	
			
if __name__ == '__main__':
	from http.server import HTTPServer
	server= HTTPServer((ipaddress,1234), GetHandler)
	print("Server Starting")
	server.serve_forever()

