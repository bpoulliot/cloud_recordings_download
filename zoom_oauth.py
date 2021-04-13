#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rauth import OAuth2Service
import webbrowser, json, base64, requests

def get_token():
    with open("creds.json", "r") as creds_file:
        creds = json.load(creds_file)

    if creds["refresh_token"] != "":
        refresh_token = creds["refresh_token"]
        grant_type = "refresh_token"
    else:
        grant_type = "authorization_code"

    zoom_api = OAuth2Service(
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        name='zoom',
        authorize_url='https://zoom.us/oauth/authorize',
        access_token_url='https://zoom.us/oauth/token',
        base_url='https://api.zoom.us/v2')

    redirect_uri = "<your_redirect_url_here>"
    params = {'response_type': 'code',
              'redirect_uri': redirect_uri,
              'client_id': creds["client_id"]
              }
    if grant_type == "authorization_code":
        zoom_auth =  zoom_api.get_authorize_url(**params)

        print("Visit Zoom OAuth Page: {}".format(zoom_auth))
        webbrowser.open(zoom_auth)

        auth_uri = input("Paste callback URL: ")
        auth_code = auth_uri.split("code=", 1)[1]

    auth_str = "{}:{}".format(creds["client_id"], creds["client_secret"])
    auth_bytes = auth_str.encode("ascii")
    auth_bytes_b64 = base64.b64encode(auth_bytes)
    auth_b64 = auth_bytes_b64.decode("ascii")

    if grant_type == "authorization_code":
        data = {"grant_type": grant_type,
                "code": auth_code,
                "redirect_uri": redirect_uri
                }

    if grant_type == "refresh_token":
        data = {"grant_type": grant_type,
                "refresh_token": refresh_token
                }

    headers = {
                "Authorization": "Basic {}".format(auth_b64)
                }

    oauth_response = requests.post(zoom_api.access_token_url, headers=headers, \
                                    data=data).json()

    zoom_token = oauth_response["access_token"]
    creds["refresh_token"] = oauth_response["refresh_token"]

    new_rtoken = oauth_response["refresh_token"]
    with open("creds.json", "w") as update:
        json.dump(creds, update)

    return zoom_token
