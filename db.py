from pymongo import MongoClient
from flask import json
from math import floor
from time import time

def current_milli_time():
    return floor(time() * 1000)

client = MongoClient("mongodb+srv://admin:admin@db.ekcwb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
profiles = client.db.profiles


print('connected to db')

def createUser(username, userMail):
	profiles.insert_one({'username' : username, 'mail' : userMail})

def userExists(user):
	found = profiles.find_one({'username' : user}) or profiles.find_one({'mail' : user})
	return found != None

def userOccupied(username, userMail):
	found = profiles.find_one({'username' : username}) or profiles.find_one({'mail' : userMail})
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

def createNote(username):
	userNotes = client.notes[username]
	noteid = str(current_milli_time())
	note = {
	'username' : username,
	'text' : "", # maybe different type here
	'noteid' : noteid,
	'title' : 'Empty note',
	'accessUsers' : []
	}
	userNotes.insert_one(note)
	return noteid

def deleteNote(username, noteid):
	userNotes = client.notes[username]
	note = {
	'username' : username,
	'noteid' : noteid
	}
	note = userNotes.find_one(note)
	if not note:
		return json.dumps({'success' : False, 'error' : 'note does not exist'})
	userNotes.delete_one(note)
	return json.dumps({'success' : True})

def modifyNote(username, noteid, text, newTitle):
	userNotes = client.notes[username]
	note = userNotes.find_one({'noteid' : noteid})
	if not note:
		return json.dumps({'sucess' : False, 'error' : 'note does not exist'})
	userNotes.update_one(note, {'$set': {'text' : text, 'title': newTitle}})
	# userNotes.delete_one(note)
	# note.note = text
	# note.title = newTitle
	# note = {
	# 'username' : username,
	# 'note' : text,
	# 'noteid' : noteid,
	# 'title' : newTitle
	# }
	# userNotes.insert_one(note)
	return json.dumps({'sucess' : True})

def modifyNoteAccess(username, noteid, newAccessUsers):
	userNotes = client.notes[username]
	note = userNotes.find_one({'noteid' : noteid})
	if not note:
		return json.dumps({'sucess' : False, 'error' : 'note does not exist'})
	userNotes.update_one(note, {'$set': {'accessUsers' : newAccessUsers}})
	# userNotes.delete_one(note)

	# note = {
	# 'username' : username,
	# 'note' : text,
	# 'noteid' : noteid,
	# 'title' : newTitle
	# }
	# note.accessUsers = newAccessUsers
	# userNotes.insert_one(note)
	return json.dumps({'sucess' : True})

def getNoteAccessUsers(username, noteid):
	userNotes = client.notes[username]
	note = userNotes.find_one({'noteid' : noteid})
	if not note:
		return json.dumps({'sucess' : False, 'error' : 'note does not exist'})
	return json.dumps({'accessUsers' : note.accessUsers, 'sucess' : True})

def addNoteAccessUser(username, noteid, accessUser):
	userNotes = client.notes[username]
	note = userNotes.find_one({'noteid' : noteid})
	if not note:
		return json.dumps({'sucess' : False, 'error' : 'note does not exist'})
	accessUsers = note.accessUsers
	if accessUser not in accessUsers:
		accessUsers.append(accessUser)
	userNotes.update_one(note, {'$set': {'accessUsers' : accessUsers}})
	return json.dumps({'sucess' : True})

def removeNoteAccessUser(username, noteid, accessUser):
	userNotes = client.notes[username]
	note = userNotes.find_one({'noteid' : noteid})
	if not note:
		return json.dumps({'sucess' : False, 'error' : 'note does not exist'})
	accessUsers = note.accessUsers
	if accessUser in accessUsers:
		accessUsers.remove(accessUser)
	else:
		return json.dumps({'sucess' : False})
	
	userNotes.update_one(note, {'$set': {'accessUsers' : accessUsers}})
	return json.dumps({'sucess' : True})

def getNotes(username):
	userNotes = client.notes[username]
	return userNotes.find({'text' : {'$exists' : True}})

