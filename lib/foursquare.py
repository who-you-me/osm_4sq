# -*- coding: utf-8 -*-

import json
import urllib
import requests

def authenticate_url(client_id, redirect_uri):
    url = "https://foursquare.com/oauth2/authenticate"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri
    }
    return url + "?" + urllib.urlencode(params)

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
        
