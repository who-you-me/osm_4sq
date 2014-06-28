# -*- coding: utf-8 -*-

from flask import Flask

from functools import wraps
from flask import render_template, request, redirect, url_for
from flask import jsonify, session
from werkzeug.contrib.cache import SimpleCache

from lib.foursquare import Foursquare

app = Flask(__name__)
app.config.from_object("settings")

CLIENT_ID = app.config["CLIENT_ID"]
CLIENT_SECRET = app.config["CLIENT_SECRET"]

app.secret_key = app.config["SECRET_KEY"]

cache = SimpleCache()

def is_login():
    return session.has_key("is_login")

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
    session["user"] = get_user()
    session["is_login"] = True

    return redirect(url_for("index"))

@app.route("/checkins")
def checkins():
    checkins = {}
    if is_login():
        checkins = get_checkins()
        return jsonify(checkins)
    return jsonify(checkins)

def get_user():
    fsq = Foursquare(session["access_token"])
    user = fsq.users()

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

def get_checkins():
    key = "checkins-%s" % session["user"]
    checkins = cache.get(key)
    if checkins:
        return checkins

    fsq = Foursquare(session["access_token"])
    raw_checkins = fsq.checkins()

    items = raw_checkins["items"]
    checkins = {"items": {}}
    center = {"lon": 0, "lat": 0}
    for item in items:
        venue = item["venue"]
        if not venue["id"] in checkins["items"]:
            checkins["items"][venue["id"]] = {
                "name": venue["name"],
                "location": {
                    "lon": venue["location"]["lng"],
                    "lat": venue["location"]["lat"]
                },
                "count": 1
            }
        else:
            checkins["items"][venue["id"]]["count"] += 1
        center["lon"] += venue["location"]["lng"]
        center["lat"] += venue["location"]["lat"]

    center["lon"] /= len(items)
    center["lat"] /= len(items)
    checkins["center"] = center

    cache.set(key, checkins, timeout=60*60)
    return checkins

if __name__ == "__main__":
    app.run(debug=True)
