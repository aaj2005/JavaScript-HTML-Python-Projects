from http.server import BaseHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse
import json
import cgi
import io
import os
import json

def updateData(newData):
	pathN= r"C:\FTP Server Files"+ '/' + "PythonJSONfile" + '.json'
	with open(pathN, 'r', encoding="utf-8") as fp:
		data=json.load(fp)
	dictData= eval(newData)
	data.append(dictData)
	createJSON(pathN,data)
	return newData
def createJSON(filename,data):
	with open(filename, 'w', encoding="utf-8") as fp:
		json.dump(data,fp)



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
			print("mimeType", mimeType)
			self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
			self.end_headers()
			path = r"C:\Users\alial\OneDrive\Desktop\Programs\JavaScript Practice Programs" + x
			with open(path,"r",encoding="utf-8") as f:
				self.wfile.write(f.read().encode("utf-8"))
		else:
			print("Else")
			pathN= "C:\FTP Server Files/PythonJSONfile.json"
			with open(pathN, 'r', encoding="utf-8") as fp:
				a = fp.read().encode("utf-8")
			parsed_path = parse.urlparse(self.path)
			self.send_response(200)
			self.send_header('Content-Type', 'application/json; utf-8')
			self.end_headers()
			self.wfile.write(a)

	def do_POST(self):
		content_length = int(self.headers.get('content-length'))
		body = self.rfile.read(content_length).decode("utf-8")
		updateData(body)
		self.send_response(200)
		print("send_response check")
		self.send_header('Content-Type', 'text/javascript; utf-8')
		print("send_header check")
		self.end_headers()
		print("end_headers check")
		print("h")
		print("data Updated")
		print(True)
if __name__ == '__main__':
	from http.server import HTTPServer
	server= HTTPServer(('localhost',1234), GetHandler)
	print("Server Starting")
	server.serve_forever()