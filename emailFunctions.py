from flask_mail import Message, Mail

def configureEmail(app):
	app.config["MAIL_SERVER"] ='smtp.gmail.com'
	app.config["MAIL_PORT"] = 465
	app.config["MAIL_USE_TLS"] = False
	app.config["MAIL_USE_SSL"] = True
	app.config["MAIL_USERNAME"] = "geniusnotes.service@gmail.com"
	app.config["MAIL_PASSWORD"] = "Gen-Nnte82"
	app.config["MAIL_DEFAULT_SENDER"] = "geniusnotes.service@gmail.com"
	return Mail(app)

def createMessage(toMail, msgBody, header="Authorization for genius-notes"):
	return Message(
              header,
              sender = "geniusnotes.service@gmail.com",
              recipients = [toMail],
              body = msgBody
             )
