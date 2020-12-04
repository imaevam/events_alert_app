from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = True  
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "getdatafromdb@gmail.com"
app.config['MAIL_PASSWORD'] = 'ehehoz99'
app.config['MAIL_DEFAULT_SENDER'] = "getdatafromdb@gmail.com"


def sender(email, password):
    msg = Message(subject="Восстановление пароля", sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
    msg.body = "Привет. Если ты это читаешь, значит система восстановления пароля работает исправно. Твой пароль {}".format(password)
    mail.send(msg)
    return "Сообщение отправлено"
