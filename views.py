from django.shortcuts import render
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from django.contrib.auth.models import User

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


client_id = '1223734504390648'
client_secret = '6cf410ca1a57c742130c4932ee5300d6'
authorization_base_url = 'https://www.facebook.com/dialog/oauth'
token_url = 'https://graph.facebook.com/oauth/access_token'
redirect_uri = "http://127.0.0.1:8000/fb/home"
facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
facebook = facebook_compliance_fix(facebook)

def index(request):
    template='fblogin/index.html'
    authorization_url, state = facebook.authorization_url(authorization_base_url)

    return render(request, template,{'auth_url':authorization_url})


def home(request,home):
    template = 'fblogin/home.html'
    redirect_response = request.build_absolute_uri()
    facebook.fetch_token(token_url, client_secret=client_secret,authorization_response=redirect_response)
    scope = 'id,name,email,birthday,friends,last_name,first_name'
    r = facebook.get('https://graph.facebook.com/v2.8/me?fields={}'.format(scope))
    info = r.json()
    name=info['name']
    fname=info["first_name"]
    last_name=info['last_name']
    email=info['email']
    birthday=info['birthday']
    User.objects.create_user(username=name,first_name=first_name,last_name=last_name,email=email)
    return render(request,template, {'info':info})


