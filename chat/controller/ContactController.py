import sqlite3

from model.Contact import Contact


class ContactController:
    def get(self, user_id=None):
        con = sqlite3.connect("database/chatDB.db")
        cur = con.cursor()

        if user_id is None:
            res = cur.execute("SELECT * FROM Contact")

        else:
            res = cur.execute("SELECT * FROM Contact WHERE id = \"{}\"".format(user_id))

        ans = res.fetchall()
        con.close()

        contact_list: list = []
        for i in ans:
            contact = Contact(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
            contact_list.append(contact.__dict__)

        if not contact_list:
            return contact_list, 404

        return contact_list

    def create(self, data):
        try:
            con = sqlite3.connect("database/chatDB.db")
            cur = con.cursor()
            cur.execute("INSERT INTO Contact(nome, email, telefone, endereco, bairro, cidade, estado) "
                        "values (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(data['nome'], data['email'],
                                                                     data['telefone'], data['endereco'],
                                                                     data['bairro'], data['cidade'],
                                                                     data['estado']))
            con.commit()
            con.close()
            return "Criado com sucesso!"
        
        except sqlite3.OperationalError:
            return "Houve um erro ao adicionar ao banco de dados."

    def update(self, user_id, data):
        try:
            con = sqlite3.connect("database/chatDB.db")
            cur = con.cursor()
            for i in data.keys():
                cur.execute("Update Contact set {} = \"{}\" where id = \"{}\"".format(i, data[i], user_id))
                con.commit()
            con.close()
            return "Atualizado com sucesso!"

        except sqlite3.OperationalError as e:
            return "Houve um erro ao atualizar os dados do usuário.", 400

    def delete(self, user_id):
        try:
            con = sqlite3.connect("database/chatDB.db")
            cur = con.cursor()
            cur.execute("DELETE FROM Contact WHERE id = \"{}\"".format(user_id))
            con.commit()
            con.close()

            if cur.rowcount == 0:
                return "Usuário não encontrado.", 404

            return "Usuário removido com sucesso!"

        except sqlite3.OperationalError as e:
            return "Houve um erro ao remover os dados do usuário.", 400