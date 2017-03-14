from django.shortcuts import render
from django.http import *
import tweepy

CONSUMER_KEY = "8hEmZ6mbH41A77C3fTQO0oTci"
CONSUMER_KEY_SECRET = "ki3gTojRlS4lo8BwH6yNZzj5zUZ1lzLz0UlxiovZm852Ak7OPs"
access_token = ''
access_token_secret = ''

def index(request):
    auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_KEY_SECRET)
    auth_url=auth.get_authorization_url(True)
    request.session['request_token'] = auth.request_token
    response = HttpResponseRedirect(auth_url)
    return response
    
def about(request):
    verifier = request.GET.get('oauth_verifier')
    request_token = request.session['request_token']
    del request.session['request_token']
    auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_KEY_SECRET)
    auth.request_token = request_token
    auth.get_access_token(verifier)
    request.session['token'] = (auth.access_token, auth.access_token_secret)
    print auth.access_token+"hello"
    api = tweepy.API(auth)
    api.update_status('tweepy + oauth!')
    return HttpResponse("Click me <a href='/tfetcher/index'>back</a>")
