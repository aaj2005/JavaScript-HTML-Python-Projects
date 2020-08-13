class accounts:
	def __init__(self,accountID,firstName,lastName,dateOfBirth,username,password,email,active,package):
		self.Id=accountID
		self.first=firstName
		self.last=lastName
		self.date=dateOfBirth
		self.user=username
		self.password=password
		self.email=email
		self.status=active
		self.package=package
		self.accountArr=[self.Id,self.first,self.last,self.date,self.user,self.password,self.email,self.status,self.package]
	def __repr__(self):
		return 'accounuts'+str(tuple(self.accountArr))
	def __str__(self):
		return "{} {}: {}".format(self.first,self.last,self.Id)

class users:
	def __init__(self,userId,profileName,restriction):
		self.userId=userId
		self.profName=profileName
		self.accountId=accountId
		self.restriction=restriction
		self.userArr=[self.userId,self.profName,self.last,self.accountId,self.restriction]
	def __repr__(self):
		return 'users'+str(tuple(self.userArr))
	def __str__(self):
		return "{} {}: {}".format(self.profName,self.userId,self.accountId)


class tvShows:
	def __init__(self,showID,name,releaseDate,category,runTime,expiry,restriction):
		self.showID=showID
		self.name=name
		self.releaseDate=releaseDate
		self.category=category
		self.runTime=runTime
		self.expiry=expiry
		self.restriction=restriction
		self.showArr=[self.showID,self.name,self.releaseDate,self.category,self.runTime,self.expiry,self.restriction]
	def __repr__(self):
		return 'tvShows'+str(tuple(self.showArr))
	def __str__(self):
		return "{}: {}".format(self.name,self.showId)


class myList:
	def __init__(self,showId,userId):
		self.showId=showId
		self.userId=userId
