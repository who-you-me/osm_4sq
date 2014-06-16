# -*- coding: utf-8 -*-

import json
import time
import urllib
import requests

class Foursquare(object):
    BASEURL = "https://api.foursquare.com/v2"

    @staticmethod
    def authenticate_url(client_id, redirect_uri):
        url = "https://foursquare.com/oauth2/authenticate"
        params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri
        }
        return url + "?" + urllib.urlencode(params)

    @staticmethod
    def get_access_token(client_id, client_secret, redirect_uri, code):
        url = "https://foursquare.com/oauth2/access_token"
        params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code
        }
        resp = requests.get(url, params=params)
        content = json.loads(resp.text)
        return content["access_token"]

    def __init__(self, oauth_token):
        self.oauth_token = oauth_token
        self.version = self.get_version()

    def handle_request(self, path, method, **params):
        url = self.BASEURL + path
        params["oauth_token"] = self.oauth_token,
        params["v"] = self.version
        if method == "GET":
            resp = requests.get(url, params=params)
        elif method == "GET":
            resp = requests.post(url, params=params)
        return json.loads(resp.text)

    def get_version(self):
        return time.strftime("%Y%m%d")

    def users(self, user_id=None):
        method = "GET"
        if not user_id:
            user_id = "self"
        path = "/users/%s" % user_id
        resp = self.handle_request(path, method)
        return resp["response"]["user"]

    def checkins(self):
        method = "GET"
        path = "/users/self/checkins"
        resp = self.handle_request(path, method, limit=250)
        return resp["response"]["checkins"]

