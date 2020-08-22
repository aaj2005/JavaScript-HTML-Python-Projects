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
	c.execute("""CREATE Table IF NOT EXISTS accounts (
				accountID INTEGER PRIMARY KEY, 
				firstName nvarchar(25),
				lastName nvarchar(30),
				dateOfBirth date,
				username nvarchar(60),
				password nvarchar(60),
				email nvarchar(320),
				active BOOLEAN,
				package nvarchar(300)
				)""")
	c.execute("""CREATE Table IF NOT EXISTS users (
				userID int,
				profileName nvarchar(30),
				accountID int,
				restriction nvarchar(10),
				userAccountCombination nvarchar(100) PRIMARY KEY,
				FOREIGN KEY(accountID) REFERENCES accounts(accountID)
				)""")
	c.execute("""CREATE Table IF NOT EXISTS myList (
				showID int,
				userAccountCombo nvarchar(100),
				showUserCombination int PRIMARY KEY,
				FOREIGN KEY(showID) REFERENCES tvShows(showID),
				FOREIGN KEY(userAccountCombo) REFERENCES users(userAccountCombination)
				)""")
	c.execute("""CREATE Table IF NOT EXISTS tvShows (
				showID INTEGER PRIMARY KEY, 
				name nvarchar(150),
				releaseDate date,
				category nvarchar(100),
				runTime int,
				expiry date,
				restriction int
				)""")
def getMaxValue(column,table):
	connectToDataBase()
	c.execute("SELECT MAX("+column+") FROM "+table)
	return c.fetchall()
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
	allShows={}
	for x in showData:
		allShows[x[1]]=classes.tvShows(x[0],x[1],x[2],x[3],x[4],x[5],x[6])
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
	allLists={}
	for x in listData:
		userAccountArr=x[1].split(':')
		c.execute("SELECT username FROM accounts WHERE accountID=:accountID",{'accountID':userAccountArr[0]})
		accountName=c.fetchall()[0][0]
		c.execute("SELECT profileName FROM users WHERE accountID=:accountID and userID=:userID",{'accountID':userAccountArr[0],'userID':userAccountArr[1]})
		userName=c.fetchall()[0][0]
		allLists[accountName+':'+userName+':'+str(x[0])]=classes.myList(x[0],x[1],x[2])
	
	conn.close()
	return allLists
def insertAccounts(ID, firstName, lastName, dateOfBirth, username, password, email, active, package):
	connectToDataBase()
	with conn:
		c.execute("INSERT INTO accounts VALUES (:ID, :firstName, :lastName, :dateOfBirth, :username, :password, :email, :active, :package)",
		{'ID':ID, 'firstName':firstName, 'lastName':lastName, 'dateOfBirth':dateOfBirth, 'username':username, 'password':password, 'email':email, 'active':active, 'package':package})
	conn.commit()
	conn.close()

def insertUsers(userID, profileName, accountID, restriction):
	connectToDataBase()
	with conn:
		c.execute("INSERT INTO users VALUES (:userID, :profileName, :accountID, :restriction,:userAccountCombo)",
		{'userID':userID, 'profileName':profileName, 'accountID':accountID, 'restriction':restriction,'userAccountCombo':str(accountID)+':'+str(userID)})
	conn.commit()
	conn.close()

def updateAccountsInfo(updatedItem, updatedValue, ID):
	connectToDataBase()
	with conn:
		c.execute("UPDATE accounts SET "+updatedItem+' = '+ "'"+updatedValue+"'"+' WHERE ID = '+ ID)
	conn.commit()
	conn.close()

def  insertShows(showID, showName, releaseDate, category, runTime, expiry, restriction):
	connectToDataBase()	
	with conn:
		c.execute("INSERT INTO tvShows VALUES (:showID,:name,:releaseDate,:category,:runTime,:expiry,:restriction)",
		{'showID':showID, 'name':showName, 'releaseDate':releaseDate, 'category':category, 'runTime':runTime, 'expiry':expiry, 'restriction':restriction})
	conn.commit()
	conn.close()
def  updateShows(showID, showName, releaseDate, category, runTime, expiry, restriction):
	connectToDataBase()	
	with conn:
		c.execute("UPDATE tvShows SET showID=:showID,name=:name,releaseDate=:releaseDate,category=:category,runTime=:runTime,expiry=:expiry,restriction=:restriction WHERE showID="+showID,
		{'showID':showID, 'name':showName, 'releaseDate':releaseDate, 'category':category, 'runTime':runTime, 'expiry':expiry, 'restriction':restriction})
	conn.commit()
	conn.close()

def addToList(showID, accountID, userID):
	connectToDataBase()
	with conn:
		userAccountCombo= str(accountID)+':'+str(userID)
		showUserCombination=getMaxValue('showUserCombination','myList')[0][0]
		if showUserCombination== None:
			showUserCombination=0
		c.execute("INSERT INTO myList VALUES (:showID, :userAccountCombo, :showUserCombination)",
		{'showID':showID,'userAccountCombo':userAccountCombo,'showUserCombination':showUserCombination+1})
		conn.commit()

	conn.close()
def retrieveData(table,selection,inputID="", email="",movieName="",showId='',userId=''):
	connectToDataBase()
	if inputID!='' and showId!='' and userId!='':
		with conn:
			userAccountCombo=str(inputID)+':'+str(userId)
			c.execute("SELECT "+selection+" FROM "+table+" WHERE userAccountCombo=:userAccountCombo AND showId=:showId",
			{'userAccountCombo':userAccountCombo,'showId':showId})
			return c.fetchall()
		conn.close()
	elif showId != '':
		with conn:
			c.execute("SELECT "+selection+" FROM "+table+" WHERE showID="+str(showId))
			return c.fetchall()
		conn.close()
	elif movieName != '':
		with conn:
			c.execute("SELECT "+selection+" FROM "+table+" WHERE name=:movieName",
			{'movieName':movieName})
			return c.fetchall()
		conn.close()
	elif inputID=='' and movieName=='':
		with conn:
			c.execute("SELECT "+selection+" FROM "+table+" WHERE username=:username OR email=:email",
			{'username':email,'email':email})
			return c.fetchall()
		conn.close()


def getMaxValueUsers(column,table,accountID):
	connectToDataBase()
	with conn:
		c.execute("SELECT MAX("+column+") FROM "+table+" WHERE accountID="+str(accountID))
		return c.fetchall()
def removeShowFromList(showId,userAccountCombo):
	connectToDataBase()
	with conn:
		c.execute("DELETE FROM myList WHERE showId=:showId AND userAccountCombo=:userAccountCombo",{'showId':showId,'userAccountCombo':userAccountCombo})

def delTable():
	c.execute("DROP TABLE myList")
	c.execute("DROP TABLE users")
	c.execute("DROP TABLE accounts")
	c.execute("DROP TABLE tvShows")
	pass

connectToDataBase()

# delTable()
# createTable()
# insertAccounts(1,"Ali","AlJishi","2005-04-25", 'aaj2005', 'ali2005', 'botbyali5@gmail.com', 'True', 'UHD')
# insertUsers(4, 'Salman', 2, '15')

# c.execute("DELETE FROM tvShows where showId>=3")
conn.commit()
