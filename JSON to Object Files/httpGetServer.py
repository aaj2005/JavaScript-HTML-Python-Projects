from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
import io
import os
import json
from ftplib import FTP
import sched, time
import getpass
JSONFileName=1

print("Username:")
user = input()
password = getpass.getpass()
ftp = FTP("192.168.100.52")
ftp.login(user,password)
def returnStoredFile(passedContent):
	global returnedFTPData
	returnedFTPData = passedContent
def getInt(listInput):
	b=0
	newList=[]
	for p in listInput:
		try:
			newList.append(int(listInput[b]))
			b+=1
		except:
			b+=1
			continue
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
			path = r"C:\Users\alial\OneDrive\Desktop\Programs\JavaScript Practice Programs" + x
			with open(path,"r",encoding="utf-8") as f:
				self.wfile.write(f.read().encode("utf-8"))
		else:
			pathN= "C:\FTP Server Files/PythonJSONfile.json"
			with open(pathN, 'r', encoding="utf-8") as fp:
				a = fp.read().encode("utf-8")
			parsed_path = parse.urlparse(self.path)
			self.send_response(200)
			self.send_header('Content-Type', 'application/json; utf-8')
			self.end_headers()
			self.wfile.write(a)

	def do_POST(self):
		global JSONFileName
		content_length = int(self.headers.get('content-length'))
		body = self.rfile.read(content_length)
		decodedBody = body.decode("utf-8")
		if  decodedBody == 'loadDropDown':
			a=[]
			z=0
			for x in ftp.nlst():
				a.append(x)
				a[z]=os.path.splitext(a[z])
				a[z]=a[z][0]
				z+=1
			updatedList=getInt(a)
			JSONFileName = max(updatedList)
			self.send_response(200)
			self.send_header('Content-Type', 'text/strings; utf-8')
			self.end_headers()
			self.wfile.write(str(JSONFileName).encode("utf-8"))
		elif str(decodedBody) <= str(JSONFileName):
			print(ftp)
			ftp.retrbinary('RETR '+decodedBody+".json",returnStoredFile)
			parsed_path = parse.urlparse(self.path)
			self.send_response(200)
			self.send_header('Content-Type', 'application/json; utf-8')
			self.end_headers()
			self.wfile.write(returnedFTPData)
		else:
			updateData(body,JSONFileName+1)
			self.send_response(200)
			self.send_header('Content-Type', 'text/javascript; utf-8')
			self.end_headers()
			JSONFileName+=1
if __name__ == '__main__':
	from http.server import HTTPServer
	server= HTTPServer(('localhost',1234), GetHandler)
	print("Server Starting")
	server.serve_forever()