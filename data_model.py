from werkzeug.security import generate_password_hash

class user_db(object):
	"""docstring for user_db"""
	def __init__(self, name, passwd,new_user=False):
		self.name = name
		if new_user:
			self.passwd = str(generate_password_hash(passwd))
		self._passwd = passwd

	def dict(self):
	    return {"name":self.name, "passwd":self.passwd}
	