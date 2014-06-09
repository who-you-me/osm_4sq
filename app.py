# -*- coding: utf-8 -*-

from flask import Flask

from functools import wraps
from flask import g, request, redirect, url_for

app = Flask(__name__)

def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
#        if g.user is None:
        if True:
            return redirect(url_for("login", next=request.path))
        return func(*args, **kwargs)
    return decorated

@app.route("/")
@login_required
def index():
    return "Hello"

@app.route("/login")
def login():
    return "login"

if __name__ == "__main__":
    app.run(debug=True)
