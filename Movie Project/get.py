import os
import sys
sys.path.append('database')
import SQLite
def sendResponse(self,responseCode,keyword,mime,data):
	self.send_response(responseCode)
	self.send_header(keyword, mime)
	self.end_headers()
	self.wfile.write(data)
	
def loadDropDown():
	maxID=SQLite.getMaxValue("showID", "tvShows")
	listInStr = ""
	try:
		listInStr= maxID[0][0]
	except:
		listInStr="No Data Stored"
	return listInStr
def openRequest(self,x,url,body=None,responseCode=200):
	print(x,"XXX")
	mimeType= os.path.splitext(x)
	dictionary={
		"html":"text/html",
		"js":"text/javascript",
		'css':"text/css",
		'jpg':"image/jpeg"
	}
	self.send_response(responseCode)
	self.send_header('Content-Type', dictionary[mimeType[1][1:]] +'; utf-8')
	self.end_headers()
	print(dictionary[mimeType[1][1:]])
	if body is None:
		path = r"C:\Users\alial\Desktop\Programs\JavaScript Practice Programs\Movie Project\src"+ url + x
		with open(path,"r",encoding="utf-8") as f:
			self.wfile.write(f.read().encode("utf-8"))
	else:
		self.wfile.write(body.encode("utf-8"))