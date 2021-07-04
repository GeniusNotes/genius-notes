from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@db.ekcwb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
profiles = client.db.profiles


def createUser(username, userMail):
	profiles.insert_one({'username' : username, 'mail' : userMail})

def userExists(user):
	found = profiles.find_one({'username' : username}) or profiles.find_one({'mail' : user})
	return found != None

def getData(user):
	if '@' in user:
		# email given; find username
		username = profiles.find_one({'mail' : user})['username']
		userMail = user
	else:
		# username given; find email
		username = user
		userMail = profiles.find_one({'username' : user})['mail']
	return username, userMail

