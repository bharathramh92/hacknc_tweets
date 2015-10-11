from django.http import HttpResponseRedirect
from django.shortcuts import render
from tweet.forms import SearchForm
from tweet.bluemix_sensitive import *
import urllib.parse
import json
from collections import defaultdict
import requests

# Create your views here.


def open_url(search):

    top_level_url = twitter_search_base_url + "?q=" + urllib.parse.quote(search, safe='') + "&size=10"
    r = requests.get(top_level_url, auth= (twitter_username, twitter_password))
    data_json = r.json()
    hashtags = defaultdict(int)
    for tweet in data_json['tweets']:
        tw = tweet['message']['body']
        # print(tw)
        for word in tw.split():
            if word[0] == "#":
                hashtags[word.lower()] += 1
    print(hashtags)
    ht = {}
    for k,v in hashtags.items():
        ht[k] = v
    return hashtags



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
            print(search)
            # o = twitter_search_url + "?q=" + urllib.parse.quote(search, safe='') + "&size=10"
            # o = "https://b66707bb-5e6b-48fa-be61-116b4274081b:ndTn1LNeKx@cdeservice.mybluemix.net/api/v1/messages/search?q=kerala%20blasters&size=10"
            # print(o)
            hashtags = open_url(search)
            return render(request, 'tweet/search_result.html', {'hashtags': dict(hashtags)})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'tweet/index.html', {'form': form})