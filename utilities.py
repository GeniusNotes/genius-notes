import random

def randRange(a, b):
	return random.randint(a, b)

def getCode(length):
	code = ""
	for _ in range(length):
		code += str(randRange(0, 9))
	return code
