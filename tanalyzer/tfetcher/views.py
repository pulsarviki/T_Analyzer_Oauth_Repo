from django.shortcuts import *
from django.http import *
from datetime import datetime,timedelta
import json
import tweepy
import mylinks
import time

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

def hashtaganalysis(request,hashtag):
    output=''
    impressions=0
    engagement=0
    engagementrate=0
    datelist={}
    for i in range(31):
        datelist[i]=00
    boldval=retrievetweetlot(hashtag,5017)
    for bold in boldval:
        impressions+=bold.author.followers_count
        engagement+=bold.favorite_count+bold.retweet_count
        for eachdate in datelist:
            print bold.created_at
            if bold.created_at.strftime('%d') == str(eachdate).zfill(2):
                datelist[eachdate]+=1
    #NEXT TASK Calculate daily impressions
    #for each in datelist:
    #    print str(each)+" "+str(datelist[each])
    engagementrate=float(engagement)/(impressions)
    print "engagementrate "+str(engagementrate)
    output=" Total Responses "+str(len(boldval))
    output+='<br/>'+" Total Impressions "+str(impressions)
    output+='<br/>'+" Total Engagement "+str(engagement)
    output+='<br/>'+" Total Engagement Rate "+str(engagementrate)
    return HttpResponse(output)

def retrievetweetlot(hashtag,_count):
    boldval=[]
    loopcounter=_count/100
    currcounter=0
    if _count%100>0:
        extracount=_count%100
    resultset=api.search(q=hashtag,count=100,result_type='popular')
    #print len(resultset)
    rlen=len(resultset)-1
    max_id=resultset[rlen].id
    currcounter+=1
    boldval.extend(resultset)
    while loopcounter>currcounter:
        try:
            resultset=api.search(q=hashtag,count=100,result_type='popular',max_id=max_id)
        except tweepy.RateLimitError:
            print 'Exception: RateLimitError'
            time.sleep(15 * 60)
            resultset=api.search(q=hashtag,count=100,result_type='popular',max_id=max_id)
        rlen=len(resultset)-1
        max_id=resultset[rlen].id
        currcounter+=1
        boldval.extend(resultset)
    resultset=api.search(q=hashtag,count=extracount,result_type='popular',max_id=max_id)
    #print len(resultset)
    rlen=len(resultset)-1
    max_id=resultset[rlen].id
    currcounter+=1
    #print str(currcounter)+" value of currcounter"
    boldval.extend(resultset)
    return boldval
