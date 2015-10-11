from django.http import HttpResponseRedirect
from django.shortcuts import render
from tweet.forms import SearchForm
from tweet.bluemix_sensitive import *
import urllib.parse
import json
from collections import defaultdict
import requests
import datetime

# Create your views here.

class Tweet:
    def __init__(self):
        self.tweets = defaultdict(int)

    def get_tweets(self):
        return dict(self.tweets)

def open_url(search):
    today = datetime.datetime.today()
    two_days_before = today - datetime.timedelta(days=2)
    print("today ", today, " two days before ", two_days_before)
    str_tif = "%d-%02d-%02dT%02d:%02d:%02dZ" %(two_days_before.year, two_days_before.month, two_days_before.day, \
                     two_days_before.hour, two_days_before.minute, two_days_before.second)
    top_level_url = twitter_search_base_url + "?q=" + urllib.parse.quote(search, safe='')\
                    + "%20AND%20posted:" + urllib.parse.quote(str_tif, safe='') \
                    + "&size=100"
    print("url ", top_level_url)
    r = requests.get(top_level_url, auth= (twitter_username, twitter_password))
    tweet_list, tweets_raw_list = [], []
    hashtags = defaultdict(int)
    if r.status_code == 200:
        data_json = r.json()
        for tweet in data_json['tweets']:
            tw = tweet['message']['body']
            tweets_raw_list.append(tw)
            t = Tweet()
            for word in tw.split():
                if word[0] == "#":
                    hashtags[word.lower()] += 1
                    t.tweets[word.lower()] += 1
            tweet_list.append(tweet_list)
    return dict(hashtags), tweets_raw_list





def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            search = form.cleaned_data['search']
            hashtags, tweets_raw_list = open_url(search)
            return render(request, 'tweet/search_result.html', {'hashtags': hashtags, 'tweets_raw_list': tweets_raw_list})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'tweet/index.html', {'form': form})