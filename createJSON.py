import json

def updateData(newData):
	dictData= eval(newData)
	data.append(dictData)
	createJSON("PythonJSONfile",data)
	return newData
def createJSON(filename,data):
	pathN= r"C:\FTP Server Files"+ '/' + filename + '.json'
	with open(pathN, 'w', encoding="utf-8") as fp:
		json.dump(data,fp)


path = './'
filename="PythonJSONfile"
data =[]


createJSON(filename,data)