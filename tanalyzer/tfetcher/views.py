from django.shortcuts import *
from django.http import *
import tweepy
import mylinks

CONSUMER_KEY = mylinks.CONSUMER_KEY
CONSUMER_KEY_SECRET = mylinks.CONSUMER_KEY_SECRET
access_token = ''
access_token_secret = ''

def home(request):
    return render(request,"tfetcher/tfetcher1home.html")

def index(request):
    auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_KEY_SECRET)
    auth_url=auth.get_authorization_url(True)
    print auth_url
    request.session['request_token'] = auth.request_token
    print auth.request_token
    response = HttpResponseRedirect(auth_url)
    return response

def about(request):
    global api
    verifier = request.GET.get('oauth_verifier')
    request_token = request.session['request_token']
    del request.session['request_token']
    auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_KEY_SECRET)
    auth.request_token = request_token
    auth.get_access_token(verifier)
    request.session['token'] = (auth.access_token, auth.access_token_secret)
    print auth.access_token+"hello"
    api = tweepy.API(auth)
    context={"boldmessage":api.home_timeline()}
    return render(request,"tfetcher/tfetcher1.html",context)

def tweets(request):
    context={"boldmessage":api.home_timeline()}
    return render(request,"tfetcher/tfetcher1.html",context)

def hashtagsearch(request,hashtag='',page=10):
    print hashtag
    print page
    context={"boldmessage":""}
    if hashtag is not '':
        boldval=api.search(q=hashtag,count=page)
        context={"boldmessage":boldval,"len":len(boldval),"page":page}
    return render(request,"tfetcher/tfetcher1hashtag.html",context)
