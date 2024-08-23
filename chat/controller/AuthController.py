import json
import sqlite3

from model.Contact import Contact


class AuthController:
    def __init__(self, cookie):
        self.__isLogged = False
        self.__id = 0

        if cookie.get("user_id"):
            auth = open("database/auth.json", "r")
            jload = auth.read()
            jload = json.loads(jload)
            auth.close()

            if jload['idLoggeds'].count(int(cookie.get("user_id"))) == 0:
                return

            self.__isLogged = True

    @property
    def logged(self):
        return self.__isLogged

    @property
    def id(self):
        return self.__id

    def login(self, name, email):
        con = sqlite3.connect("database/chatDB.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM Contact WHERE nome = \'{}\' AND email = \'{}\'".format(name, email))
        ans = res.fetchall()
        con.close()

        auth = open("database/auth.json", "r")
        jload = auth.read()
        jload = json.loads(jload)
        auth.close()

        try:
            if jload['idLoggeds'].count(ans[0][0]) == 1:
                return 400
        except IndexError:
            pass

        if not ans:
            return 404

        auth = open("database/auth.json", "w")
        contact = Contact(ans[0][0], ans[0][1], ans[0][2], ans[0][3], ans[0][4], ans[0][5], ans[0][6], ans[0][7])
        jload['idLoggeds'].append(contact.id)
        auth.write(json.dumps(jload))
        auth.close()
        self.__id = contact.id

        return 200
