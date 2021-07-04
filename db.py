from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@db.ekcwb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
profiles = client.db.profiles


def userExists(username, password):
	user = profiles.find_one({'username' : username, 'password' : password})
	if user != None:
		return True
	return False

def createUser(username, password):
	profiles.insert_one({'username' : username, 'password' : password})

def loginExists(username):
	user = profiles.find_one({'username' : username})
	if user != None:
		return True
	return False 