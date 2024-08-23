import sqlite3
from datetime import datetime

from model.Message import Message
from service.MessageService import MessageService


class MessageController:
    def send(self, message, sender, receiver):
        self.message = Message(datetime.now(), message, sender, receiver)

        try:
            con = sqlite3.connect("database/chatDB.db")
            cur = con.cursor()
            cur.execute("INSERT INTO Message(date, content, send, receiver) "
                        "values (\"{}\", \"{}\", \"{}\", \"{}\")"
                        .format(self.message.date_time, self.message.content,
                                self.message.sender, self.message.receiver))
            con.commit()
            con.close()
            return "Mensagem armazenada com sucesso!", 200

        except sqlite3.OperationalError:
            return "Houve um erro ao adicionar ao banco de dados.", 400

    def get_all(self, sender: int, receiver: int):
        message_list = MessageService().get_messages(sender, receiver)
        return message_list
