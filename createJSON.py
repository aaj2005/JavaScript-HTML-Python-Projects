import json

def createJSON(filename,data):
	pathN= "C:\FTP Server Files"+ '/' + filename + '.json'
	with open(pathN, 'w', encoding="utf-8") as fp:
		json.dump(data,fp)

path = './'
filename="PythonJSONfile"
data ={}
data['Item1'] = 'Item1 Property'
data['Item2'] = 'Item2 Property'

createJSON(filename,data)