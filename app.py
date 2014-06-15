# -*- coding: utf-8 -*-

from flask import Flask

from functools import wraps
from flask import render_template, request, redirect, url_for
from flask import session

from lib.foursquare import Foursquare

app = Flask(__name__)
app.config.from_object("settings")

CLIENT_ID = app.config["CLIENT_ID"]
CLIENT_SECRET = app.config["CLIENT_SECRET"]

app.secret_key = app.config["SECRET_KEY"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    callback = url_for("authenticate", _external=True)
    redirect_to = Foursquare.authenticate_url(CLIENT_ID, callback)
    return redirect(redirect_to)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/authenticate")
def authenticate():
    callback = url_for("authenticate", _external=True)
    code = request.args["code"]

    access_token = Foursquare.get_access_token(
        CLIENT_ID, CLIENT_SECRET,
        callback, code
    )

    session["access_token"] = access_token
    session["user"] = get_user(access_token)
    session["is_login"] = True
    return redirect(url_for("index"))

def get_user(access_token):
    fsq = Foursquare(access_token)
    user = fsq.users()
    print user

    if user.get("lastName"):
        name = user["lastName"] + " " + user["firstName"]
    else:
        name = user["firstName"]
    photo = user["photo"]["prefix"] + "60x60" + user["photo"]["suffix"]

    result = {
        "name": name,
        "photo": photo,
        "bio": user["bio"],
        "homeCity": user["homeCity"]
    }

    return result

if __name__ == "__main__":
    app.run(debug=True)
