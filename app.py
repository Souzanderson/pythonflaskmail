from flask import Flask, redirect, url_for, request, jsonify, Response, render_template
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
import json 

app = Flask(__name__) 
cors = CORS(app, resources={r"/": {"origins": "http://localhost:4200"}})

configmail = json.loads(open('config.json','r').read())

app.config['MAIL_SERVER']= configmail["server"]
app.config['MAIL_PORT'] = configmail["port"]
app.config['MAIL_USERNAME'] = configmail["user"]
app.config['MAIL_PASSWORD'] = configmail["passw"]
app.config['MAIL_USE_TLS'] = configmail["tls"]
app.config['MAIL_USE_SSL'] = configmail["ssl"]

mail = Mail(app)

@app.route("/") 
@cross_origin(origin='http://localhost:4200',headers=['Content- Type','Authorization'])
def home(): 
    # print(request.base_url)
    return "API Mail - V.0.0.1"

@app.route("/mail", methods=['POST']) 
@cross_origin(origin='http://localhost:4200',headers=['Content- Type','Authorization'])
def mailsend(): 
    try:
        body = request.json
        msg = Message(body['subject'], sender = body['from'], recipients = [body['to']])
        msg.body = body['message']
        mail.send(msg)
        return jsonify({"message":"Email enviado!"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Erro ao enviar email!"})


if __name__ == '__main__':
    app.run()