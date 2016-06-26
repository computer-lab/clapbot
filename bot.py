
import tweepy #https://github.com/tweepy/tweepy
import json
from pprint import pprint
from time import sleep
import os

def twitter_api(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def creds():
  with open('creds.json') as data_file:
        data = json.load(data_file)
        consumer_key = data['creds'][0]['consumer_key']
        consumer_secret = data['creds'][0]['consumer_secret']
        access_token = data['creds'][0]['access_token']
        access_token_secret = data['creds'][0]['access_token_secret']
        #return consumer_key, consumer_secret
        return consumer_key, consumer_secret, access_token, access_token_secret

def listen(consumer_key, consumer_secret, access_key, access_secret,since_id):


  #authorize twitter, initialize tweepy
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_key, access_secret)
  api = tweepy.API(auth)
  mentions = api.mentions_timeline(count=200,since_id=since_id)
  return mentions

def clap(tweet,user):
	clap_emoji = u"\U0001F44F"
	tweet = tweet.replace('@clapbot','').strip()
	words = tweet.split(' ')
	first_word = words[0]
	words.pop(0)
	clap_tweet = first_word
	for w in words:
		clap_tweet = clap_tweet + ' ' + clap_emoji + ' ' + w
	if len(clap_tweet) < 141:
		return clap_tweet + ' @' + user
	else:
		return 'cannot clap dat'


print clap('@clapbot i love every single gatorade flavor','mrbotsnet')
consumer_key, consumer_secret, access_key, access_secret = creds()
seen = []
log = open('log.txt','r')
for l in log:
  last = int(l)
  seen.append(last+1)
log.close()
log = open('log.txt','ab')
while len(seen) > 0:
  last_mention = max(seen)
  try:
    mentions =  listen(consumer_key, consumer_secret, access_key, access_secret,last_mention)
  except Exception as e:
    print str(e)
    print 'some sort of drama when listening'
    sleep(420)
    pass
  if len(mentions) < 1:
    sleep(420)
    print 'no new mentions, taking a 420 second break'
  else:
    for i in mentions:
      request_id = i.id_str
      seen.append(int(request_id)+1)
      log.write(request_id + '\n')
      json_tweet = json.dumps(i._json)
      json_tweet = json.loads(json_tweet)
      print json_tweet['user']['name']
      screen_name = json_tweet['user']['name']
      tweet = clap(i.text,screen_name)
      api = twitter_api(consumer_key, consumer_secret, access_key, access_secret)
      # try:

      api.update_status(status=tweet)
      print 'tweeted '+tweet
      sleep(30)
      # except Exception:
      #   print 'couldnt tweet'
      #   sleep(30)
      #   pass