import sqlite3
from datetime import date, datetime

from model.Message import Message


def search_messages(sender: int, receiver: int):
    con = sqlite3.connect("database/chatDB.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM Message WHERE send = {} AND receiver  = {}".format(sender, receiver))
    ans = res.fetchall()
    con.close()

    message_list: list = []
    for i in ans:
        message = Message(i[1], i[2], i[3], i[4])
        message_list.append(message.__dict__)

    if not message_list:
        return []

    return message_list


def order_messages(message_list: list):
    date_time_orders = []
    ordered_list = []
    for i in message_list:
        date_time_orders.append(datetime.strptime(i['date_time'], "%Y-%m-%d %H:%M:%S.%f"))

    for j in sorted(date_time_orders):
        for k in message_list:
            if j == datetime.strptime(k['date_time'], "%Y-%m-%d %H:%M:%S.%f"):
                ordered_list.append(k)
                break
    return ordered_list


class MessageService:
    def get_messages(self, sender: int, receiver: int):
        sr_message_list = search_messages(sender, receiver)
        rs_message_list = search_messages(receiver, sender)
        merged_message_list = []
        for i in sr_message_list:
            merged_message_list.append(i)
        for j in rs_message_list:
            merged_message_list.append(j)

        if not merged_message_list:
            return [], 404

        merged_message_list = order_messages(merged_message_list)

        return merged_message_list
