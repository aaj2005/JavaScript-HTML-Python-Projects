from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
import io
import os
import json
from ftplib import FTP
import sched, time
import getpass

JSONFileName=0

print("Username:")
user = input()
password = getpass.getpass()

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
	ioFile=io.BytesIO(newData)
	ftp.storbinary('Stor '+str(filename)+".json", ioFile)

class GetHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		x = parse.urlparse(self.path).path
		dictionary={
			"html":"text/html",
			"js":"text/javascript"
		}
		if(x in ("/JSON-Object.html", "/JSON-Object.js")):
			self.send_response(200)
			mimeType= os.path.splitext(x)
			self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
			self.end_headers()
			path = r"C:\Users\alial\OneDrive\Desktop\Programs\JavaScript Practice Programs\JSON to Object Files" + x
			with open(path,"r",encoding="utf-8") as f:
				self.wfile.write(f.read().encode("utf-8"))
		else:
			self.send_response(200)
			self.send_header('Content-Type', 'application/json; utf-8')
			self.end_headers()
			self.wfile.write(b"")

	def do_POST(self):
		global JSONFileName
		content_length = int(self.headers.get('content-length'))
		body = self.rfile.read(content_length)
		decodedBody = body.decode("utf-8")
		global ftp
		ftp = FTP("192.168.100.40")
		ftp.login(user,password)
		if  decodedBody == 'loadDropDown':
			storedFiles=[]
			z=0
			for x in ftp.nlst():
				storedFiles.append(x)
				storedFiles[z]=os.path.splitext(storedFiles[z])
				z+=1
			updatedList=getJSON(storedFiles)
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
			self.send_response(200)
			self.send_header('Content-Type', 'text/strings; utf-8')
			self.end_headers()
			self.wfile.write(listInStr.encode("utf-8"))
		elif parse.urlparse(self.path).path == "/getName":
			ftp.retrbinary('RETR '+decodedBody+".json",returnStoredFile)
			self.send_response(200)
			self.send_header('Content-Type', 'application/json; utf-8')
			self.end_headers()
			self.wfile.write(returnedFTPData)
		elif parse.urlparse(self.path).path == "/send":
			
			updateData(body,int(JSONFileName)+1)
			self.send_response(200)
			self.send_header('Content-Type', 'text/javascript; utf-8')
			self.end_headers()
			JSONFileName+=1
if __name__ == '__main__':
	from http.server import HTTPServer
	server= HTTPServer(('localhost',1234), GetHandler)
	print("Server Starting")
	server.serve_forever()