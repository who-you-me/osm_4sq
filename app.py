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
    access_token = fsq.get_access_token(CLIENT_ID, CLIENT_SECRET, callback, code)
    session["is_login"] = True
    session["access_token"] = access_token
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
