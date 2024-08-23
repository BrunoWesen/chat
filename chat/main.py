import json

from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_cors import CORS, cross_origin

import requests as re

from controller.AuthController import AuthController
from controller.ChatController import ChatController
from controller.ContactController import ContactController
from controller.MessageController import MessageController

app = Flask(__name__, static_folder='templates/assets', )
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

HOST = "http://127.0.0.1:6060"
# HOST = "http://10.100.38.222:8080"


@app.route("/auth", methods=['GET'])
@cross_origin()
def get_auth():
    authController = AuthController(request.cookies)
    return str(authController.logged)


@app.route("/auth", methods=['POST'])
@cross_origin()
def login():
    authController = AuthController(request.cookies)

    ans = authController.login(request.form['username'], request.form['useremail'])
    if ans == 404:
        return "Usuário não encontrado"

    if ans == 400:
        return "Usuário já está logado na plataforma!"

    response = make_response(redirect(url_for('chat_page')))

    if authController.id > 0:
        response.set_cookie('user_id', str(authController.id), path="/")

    return response


# EU SEI QUE É UMA FALHA DE SEGURANÇA GRAVE!!!!
@app.route("/message", methods=['POST'])
@cross_origin()
def send_message():
    data = request.get_json()
    messageController = MessageController()
    return messageController.send(**data)


# EU SEI QUE É UMA FALHA DE SEGURANÇA GRAVE!!!!
@app.route("/message/<id_sender>/<id_receiver>", methods=['GET'])
@cross_origin()
def get_messages(id_sender, id_receiver):
    messageController = MessageController()
    return messageController.get_all(int(id_sender), int(id_receiver))


@app.route("/contact", methods=['GET'])
@cross_origin()
def get_contact():
    control = ContactController()
    return control.get()


@app.route("/contact/<user_id>", methods=['GET'])
@cross_origin()
def get_contact_with_id(user_id):
    control = ContactController()
    return control.get(user_id)


@app.route("/contact", methods=['POST'])
@cross_origin()
def post_contact():
    data = request.get_json()
    control = ContactController()
    ans = control.create(data)
    return ans


@app.route("/contact/<user_id>", methods=['PUT'])
@cross_origin()
def put_contact(user_id):
    data = request.get_json()
    control = ContactController()
    ans = control.update(user_id, data)
    return ans


@app.route("/contact/<user_id>", methods=['DELETE'])
@cross_origin()
def delete_contact(user_id):
    control = ContactController()
    ans = control.delete(user_id)
    return ans


@app.route("/chat/", methods=['GET'])
@cross_origin()
def chat_page():
    chatController = ChatController(HOST)

    if chatController.auth(request.cookies) == "False":
        return render_template("sign_in.html")

    contact_list = chatController.get_contact_list(request.cookies)

    if not contact_list:
        response = make_response(render_template("sign_in.html"))
        response.set_cookie('user_id', '', expires=0, path="/")
        return response

    return render_template("index.html", chat_id=None, name="Chat", contacts=contact_list)


@app.route("/chat/<user_id>", methods=['GET', 'POST'])
@cross_origin()
def chat(user_id):
    chatController = ChatController(HOST)

    if chatController.auth(request.cookies) == "False":
        return render_template("sign_in.html")

    contact_list = chatController.get_contact_list(request.cookies)

    if not contact_list:
        response = make_response(render_template("sign_in.html"))
        response.set_cookie('user_id', '', expires=0,path="/")
        return response

    if request.method == "POST":
        msg_json = {"message": request.form['usermsg'],
                    "sender": int(request.cookies.get("user_id")),
                    "receiver": int(user_id)}
        message_sent = re.post(HOST + "/message", json=msg_json)

        if message_sent.status_code == 400:
            return message_sent.text, 400

    for i in contact_list:
        if str(i['id']) == user_id:
            messages = re.get(HOST + "/message/"+request.cookies.get("user_id")+"/"+user_id).json()
            return render_template("index.html", chat_id=int(user_id), name=i["name"], contacts=contact_list, messages=messages)

    return render_template("index.html", chat_id=None, name="Chat", contacts=contact_list)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6060)
