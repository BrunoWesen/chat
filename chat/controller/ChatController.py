import requests as re
import json


class ChatController:
    def __init__(self, HOST):
        self.HOST = HOST

    def auth(self, cookies):
        # Auth
        auth = re.get(self.HOST + "/auth", cookies=cookies)
        return auth.text

    def get_contact_list(self, cookie):
        # Getting contacts in Database
        contacts = re.get(self.HOST + "/contact")
        contact_list = contacts.json()

        removed_qtd = 0
        for j in contact_list:
            if j['id'] == int(cookie.get("user_id")):
                contact_list.remove(j)
                removed_qtd += 1

        if removed_qtd == 0:
            return False

        return contact_list
