from flask import Flask, render_template, request, redirect, url_for, session
from model import *
from database import *
from data_model import *
from os import getenv
from werkzeug.contrib.fixers import ProxyFix

app = Flask("fake_horoscopo")
app.config["SECRET_KEY"] = "efeito_forer"
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route("/", methods=["GET", "POST"])
def index():
    form = Signo_form()
    if request.method == "POST":
        msg = data_redis().get_message()
        return render_template("mensagem.html", form=form, mensagem=msg)
    print(form.data)
    return render_template("index.html", form=form)

@app.route("/contrib", methods=["GET", "POST"])
def send_message():
    new_message = Send_message()
    msg = data_redis().get_message()
    if new_message.validate_on_submit():
        data_sql().set_text(new_message.mensagem.data)
        return redirect(url_for("index"))
    return render_template("send_message.html", msg_old=msg, new_msg=new_message)

@app.route("/login", methods=["GET","POST"])
def login_view():
    login = Login_form()
    if login.validate_on_submit():
        user = user_db(login.name.data, login.passwd.data)
        loged = data_sql().get_user(user)
        if loged:
            session["user"] = loged
            return redirect(url_for("moderate"))
    return render_template("login.html", login=login)

@app.route("/moderate", methods=["GET", "POST"])
def moderate():

    if session["user"]:
        data = data_sql().get_all_texts()
        am = Action_mod()
        
        if am.validate_on_submit():
            if am.exe.data == "accept":
                sel = am.texts.data
                db = data_sql()
                for i in sel:
                    sel_text = db.get_text(i)["text"]
                    data_redis.set_message(sel_text)
                    db.del_text(i)
                # am = Action_mod()
            elif am.exe.data == "recuse":
                for i in am.texts.data:
                    data_sql().del_text(i)
            am = None
            am = Action_mod()
            return render_template("moderate.html", actions=am)
        return render_template("moderate.html", actions=am)

    else:
        return redirect(url_for("login_view"))

if __name__ == '__main__':
    port = getenv("PORT")
    app.run(port=port)
