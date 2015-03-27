from TwitterSearch import *
import pymongo
from dateutil.parser import *
from dateutil.tz import *
from datetime import *
from alchemyapi import AlchemyAPI

client = pymongo.MongoClient('mongodb://admin:root@ds031877.mongolab.com:31877/heroku_app34284493')

alchemyapi = AlchemyAPI()

db = client.heroku_app34284493

tweets = db.tweets

count = tweets.count()
print count
if count is not 0:
    latest_id = tweets.find( {}, { 'object.tweet_id':1 } ).sort("startedAtTime").limit(1)
    latest_id_str = latest_id[count-1]['object']['tweet_id']
    latest_id_int = int(latest_id_str)
    print 'Count of documents in Mongo is not 0. It is ' + str(count) + '. Mongo is now identifying the latest tweet ID to append as a parameter to the API call.'
else:
    print 'The Mongo Database mhetwitter and collection tweets is empty. The script will now collect all tweets.'
# create a TwitterSearchOrder object
tso = TwitterSearchOrder() 
    # let's define all words we would like to have a look for
tso.set_keywords(['@mheducation'])
    # we want to see English tweets only
tso.set_language('en') 
    # and don't give us all those entity information
tso.set_include_entities(True)
if count is not 0:
    tso.set_since_id(latest_id_int)
    print latest_id_int
    print 'Since the document count is above 0, the since_id uses the parameter of the latest tweet so that only new tweets are collected.'
else:
	print 'No documents exist in the collection right now so the since_id parameter will be empty and all tweets will be collected.'
# it's about time to create a TwitterSearch object with our secret tokens
ts = TwitterSearch(
    consumer_key = 'FDke0kbk1qY4YUOa2Xw5Y0lZt',
    consumer_secret = 'MuuIUkbO5rzJBaXdbiCq7RSOSZFCBtnE5M7Yx7cAQbP7d6AUgp',
    access_token = '501332852-hMGRm1jvKp8gHHRQUETstDktSBc13KzRPglMR4DR',
    access_token_secret = '9oY0jihs3tUSy0TGnn32x1xkbezjjXpac00ReVFQyN9kE'
 )

# caliper_tweet = {
#   "@context": "http://purl.imsglobal.org/ctx/caliper/v1/MessagingEvent",
#   "@type": "MessagingEvent",
#   "startedAtTime": "{{ created_at }}",
#   ## Can be used to query Twitter API for user information
#   "actor": "uri:twitter/user/{{ user['id_str'] }}",
#   "verb": "tweetSent",
#   "object": {
#     "@type": "tweet",
#     "@id": "uri:twitter/tweet/{{ id_str}}",
#     "subtype": "tweet",
#     ## "to" should be calculated by checking in_reply_to_user_id_str is null. If it's not null, then it should be concatenated to "uri:twitter/user/" and stored in "object"['to']
#     "to": "uri:twitter/user/{{ in_reply_to_user_id_str }}",
#     "author": "uri:twitter/user/{{ user['id_str'] }}",
#     "text": "{{ text }}",
#     "parent": "uri:twitter/tweet/{{ in_reply_to_user_id_str }}",
#     ## "mentions" is an array of the caliper IDs from the user_mentions objects array
#     "mentions": ["uri:twitter/user/{{ entities[user_mentions]['id_str'] }}", "..." ],
#     ## "hashtags" is an array of the hashtag texts included in the tweet entities
#     "hashtags": ["{{ entities[hashtags][text] }}", " "]
#   }
# }

db_inserts = 0

caliper_tweet_object = {}

twitter_id_list = []

twitter_search = ts.search_tweets_iterable(tso)

# this is where the fun actually starts :)
for tweet in twitter_search:
    mentions_list = []
    hashtags_list = []
    tweet_id = ""
    caliper_tweet = {
  "@context": "http://purl.imsglobal.org/ctx/caliper/v1/MessagingEvent",
  "@type": "MessagingEvent",
  "startedAtTime": "",
  ## Can be used to query Twitter API for user information
  "actor": "",
  "verb": "tweetSent",
  "object": {
    "@type": "MessagingEvent",
    "@id": "",
    "tweet_id": "",
    "subtype": "tweet",
    ## "to" should be calculated by checking in_reply_to_user_id_str is null. If it's not null, then it should be concatenated to "uri:twitter/user/" and stored in "object"['to']
    "to": "",
    "author": "",
    "author_alias": "",
    "author_name": "",
    "text": "",
    "tweet_sentiment": 0,
    "parent": "",
    ## "mentions" is an array of the caliper IDs from the user_mentions objects array
    "user_mentions": [],
    ## "hashtags" is an array of the hashtag texts included in the tweet entities
    "hashtags": []
  }
}
    user_id = tweet['user']['id_str']
    tweet_text = tweet['text']
    ## AlchemyAPI Sentiment Analysis
    response = alchemyapi.sentiment('text', tweet_text)
    if 'score' in response['docSentiment']:
        tweet_sentiment_score = response['docSentiment']['score']


    tweet_id = tweet['id_str']
    ds = tweet['created_at']
    tweet_date = parse(ds)
    caliper_tweet['startedAtTime'] = tweet_date
    caliper_tweet['actor'] = 'student:' + tweet['user']['screen_name']
    caliper_tweet['object']['@id'] = 'https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet_id
    caliper_tweet['object']['tweet_id'] = tweet['id_str']
    if tweet['in_reply_to_user_id_str'] is None:
        caliper_tweet['object']['to'] = 'NoReply'
        caliper_tweet['object']['parent'] = 'NoReply'
    else:
        caliper_tweet['object']['to'] = 'https://twitter.com/intent/user?user_id=' + tweet['in_reply_to_user_id_str']
        if tweet['in_reply_to_status_id_str'] is None:
            caliper_tweet['object']['parent'] = 'None'
        else:    
            caliper_tweet['object']['parent'] = 'https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet['in_reply_to_status_id_str']
    caliper_tweet['object']['author'] = 'https://twitter.com/intent/user?user_id=' + tweet['user']['id_str']
    caliper_tweet['object']['author_alias'] = tweet['user']['screen_name']
    caliper_tweet['object']['author_name'] = tweet['user']['name']
    caliper_tweet['object']['text'] = unicode(tweet['text'])
    caliper_tweet['object']['tweet_sentiment'] = tweet_sentiment_score

    for x in list(tweet['entities']['hashtags']):
        hashtag = x['text']
        hashtags_list.append(hashtag)
    for x in list(tweet['entities']['user_mentions']):
        mention = x['id_str']
        mentions_list.append(mention)
    caliper_tweet['object']['user_mentions'] = mentions_list
    caliper_tweet['object']['hashtags'] = hashtags_list
 
    tweets.insert(caliper_tweet)
    
    db_inserts = db_inserts + 1
 
    # tweet_id = tweet['id_str']
    # twitter_id_list.append(tweet_id)

#
# count = tweets.count()
# latest_id = tweets.find( {}, { 'object.tweet_id':1 } ).sort("startedAtTime").limit(1)
# latest_id_str = latest_id[count-1]['object']['tweet_id']
# latest_id_int = int(latest_id_str)

print 'deadbeef'
print str(db_inserts) + " inserts made."
