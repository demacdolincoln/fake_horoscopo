import redis
import dataset
import uuid
from os import getenv
from werkzeug.security import check_password_hash as chp

class data_redis(object):
    
    host = getenv("REDIS_H")
    port = getenv("REDIS_P")
    passwd = getenv("REDIS_PW")

    @classmethod
    def get_message(self):
        r = redis.StrictRedis(host=self.host, port=self.port, password=self.passwd)
        key = r.randomkey()
        return r.get(key).decode()

    @classmethod
    def set_message(self, mensagem):
        r = redis.StrictRedis(host=self.host, port=self.port, password=self.passwd)
        key = uuid.uuid4().hex
        r.set(key, mensagem)
        

class data_sql(object):
    
    def __init__(self):
        self.host = getenv("DATABASE_URL")
        self.conn = dataset.connect(self.host)

    def _table(self, table_name):
        table = None
        try:
            table = self.conn.get_table(table_name)
        except:
            table = self.conn.create_table(table_name)
        return table


    def get_user(self, user):
        """user :-> data_model.user_db"""
        table = self._table("user")
        try:
            login = dict(table.find_one(name=user.name))
            if login and chp(login["passwd"],user._passwd):
                return login
            else:
                return False
        except:
            return False

    def set_user(self, user):
        table = self._table("user")
        table.insert(user.dict())

    def get_all_texts(self):
        table = self._table("text")
        _data = [dict(i) for i in table.all()]
        return [(str(i["id"]), i["text"]) for i in _data]

    def get_text(self, _id):
        table = self._table("text")
        return dict(table.find_one(id=_id))

    def set_text(self,text):
        table = self._table("text")
        table.insert({"text":text})

    def del_text(self,_id):
        table = self._table("text")
        table.delete(id=_id)    