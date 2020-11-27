from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

def sender(email, password):
    msg = Message("Восстановление пароля", sender="imaevam@list.ru", recipients=[email])
    msg.body = "Привет. Если ты это читаешь, значит система восстановления пароля работает исправно. Твой пароль %d" %(password)
    mail.send(msg)
    return "Message sent!"