from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
import cgi
import io
from createJSON import createJSON
print ("Access-Control-Allow-Origin: http://localhost:8000")

class GetHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		pathN= "C:\FTP Server Files/PythonJSONfile.json"
		with open(pathN, 'r', encoding="utf-8") as fp:
			f = fp.read().encode("utf-8")
		parsed_path = parse.urlparse(self.path)
		print()
		self.send_response(200)
		self.send_header('Content-Type', 'application/json; utf-8')
		self.send_header('Access-Control-Allow-Origin', 'http://localhost:8000')
		self.end_headers()
		self.wfile.write(f)

if __name__ == '__main__':
	from http.server import HTTPServer
	server= HTTPServer(('localhost',1234), GetHandler)
	print("Server Starting")
	server.serve_forever()