import sys
import sqlite3
sys.path.append('C:/Users/alial/Desktop/Programs/JavaScript Practice Programs/Movie Project')
import classes
def connectToDataBase():	
	global conn
	conn = sqlite3.connect('C:/Users/alial/Desktop/Programs/JavaScript Practice Programs/Movie Project/dataBase/database.db')
	conn.execute("PRAGMA foreign_keys=1")
	global c
	c = conn.cursor()
def createTable():
	# c.execute("""CREATE Table accounts (
	# 			accountID INTEGER PRIMARY KEY, 
	# 			firstName nvarchar(25),
	# 			lastName nvarchar(30),
	# 			dateOfBirth date,
	# 			username nvarchar(60),
	# 			password nvarchar(60),
	# 			email nvarchar(320),
	# 			active BOOLEAN,
	# 			package nvarchar(300)
	# 			)""")
	c.execute("""CREATE Table users (
				userID INTEGER NOT NULL,
				profileName nvarchar(30),
				accountID int,
				restriction nvarchar(10),
				userOrder int PRIMARY KEY,
				FOREIGN KEY(accountID) REFERENCES accounts(accountID)
				)""")
	c.execute("""CREATE Table myList (
				showID int,
				userID int,
	 			FOREIGN KEY(showID) REFERENCES tvShows(showID)
				FOREIGN KEY(userID) REFERENCES users(userID)
	 			)""")
	c.execute("""CREATE Table tvShows (
				showID INTEGER PRIMARY KEY, 
				name nvarchar(150),
				releaseDate date,
				category nvarchar(100),
				runTime int,
				expiry date,
				restriction int
				)""")

def retrAcc():
	connectToDataBase()
	c.execute("SELECT * FROM accounts")
	accountData = c.fetchall()
	allAccounts={}
	for x in accountData:
		allAccounts[x[4]]=classes.accounts(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8])
	return allAccounts
def retrShow():
	connectToDataBase()
	c.execute("SELECT * FROM tvShows")
	showData = c.fetchall()
	allShows=[]
	for x in showData:
		allShows.append(classes.tvShows(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
	conn.close()
	return allShows
def retrUsers():
	connectToDataBase()
	c.execute("SELECT userID, profileName, accountID, restriction FROM users")
	userData = c.fetchall()
	allUsers={}
	for x in userData:
		allUsers[x[1]+str(x[2])]=classes.users(x[0],x[1],x[2],x[3])
	conn.close()
	return allUsers
def retrList():
	connectToDataBase()
	c.execute("SELECT * FROM myList")
	listData = c.fetchall()
	allLists=[]
	for x in listData:
		allLists.append(classes.myList(x[0],x[1]))
	conn.close()
	return allLists
def insertAccounts(ID, firstName, lastName, dateOfBirth, username, password, email, active, package):
	connectToDataBase()
	with conn:
		c.execute("INSERT INTO accounts VALUES (:ID, :firstName, :lastName, :dateOfBirth, :username, :password, :email, :active, :package)",
		{'ID':ID, 'firstName':firstName, 'lastName':lastName, 'dateOfBirth':dateOfBirth, 'username':username, 'password':password, 'email':email, 'active':active, 'package':package})
	conn.close()

def insertUsers(userID, profileName, accountID, restriction):
	connectToDataBase()
	with conn:
		print(userID)
		c.execute("INSERT INTO users(userID,profileName,accountID,restriction) VALUES (:userID, :profileName, :accountID, :restriction)",
		{'userID':userID, 'profileName':profileName, 'accountID':accountID, 'restriction':restriction})
	conn.close()

def updateAccountsInfo(updatedItem, updatedValue, ID):
	connectToDataBase()
	with conn:
		c.execute("UPDATE accounts SET "+updatedItem+' = '+ "'"+updatedValue+"'"+' WHERE ID = '+ ID)
	conn.close()

def  insertShows(showID, showName, releaseDate, category, runTime, expiry, restriction):
	connectToDataBase()	
	with conn:
		c.execute("INSERT INTO tvShows VALUES (:showID,:name,:releaseDate,:category,:runTime,:expiry,:restriction)",
		{'showID':showID, 'name':showName, 'releaseDate':releaseDate, 'category':category, 'runTime':runTime, 'expiry':expiry, 'restriction':restriction})
	conn.close()
def  updateShows(showID, showName, releaseDate, category, runTime, expiry, restriction):
	connectToDataBase()	
	with conn:
		c.execute("UPDATE tvShows SET showID=:showID,name=:name,releaseDate=:releaseDate,category=:category,runTime=:runTime,expiry=:expiry,restriction=:restriction WHERE showID="+showID,
		{'showID':showID, 'name':showName, 'releaseDate':releaseDate, 'category':category, 'runTime':runTime, 'expiry':expiry, 'restriction':restriction})
	conn.close()

def addToList(showID, userID):
	connectToDataBase()
	with conn:
		c.execute("INSERT INTO myList VALUES (:showID,:userID)",
		{'showID':showID, 'userID':userID})
	conn.close()
def retrieveData(table,selection,inputID="", email=""):
	connectToDataBase()
	if inputID=='':
		with conn:
			c.execute("SELECT "+selection+" FROM "+table+" WHERE username=:username OR email=:email",
			{'username':email,'email':email})
			return c.fetchall()
		conn.close()
	else:
		with conn:
			c.execute("SELECT "+selection+" FROM "+table+" WHERE showID="+inputID)
			return c.fetchall()
		conn.close()

def getMaxValue(column,table):
	connectToDataBase()
	c.execute("SELECT MAX("+column+") FROM "+table)
	return c.fetchall()
def getMaxValueUsers(column,table,accountID):
	connectToDataBase()
	c.execute("SELECT MAX("+column+") FROM "+table+" WHERE accountID="+str(accountID))
	return c.fetchall()
def delTable():
	# c.execute("DROP TABLE accounts")
	c.execute("DROP TABLE users")
	# c.execute("DROP TABLE myList")
	# c.execute("DROP TABLE tvShows")


connectToDataBase()
# delTable()
# createTable()
# insertAccounts(1,"Ali","AlJishi","2005-04-25", 'aaj2005', 'ali2005', 'botbyali5@gmail.com', 'True', 'UHD')
# insertUsers(4, 'Salman', 2, '15')

# c.execute("DELETE FROM users where userID=1")
conn.commit()
