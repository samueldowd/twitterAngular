import pymongo
import simplejson
import bson
from bson import json_util
import json

client = pymongo.MongoClient('localhost', 27017)

db = client.mhetwitter

tweets = db.tweets

result_data = tweets.find( {} ).limit(20)

iterator = True

result_dict = {}

key = 1

print result_data.alive

while iterator is True:
	print iterator
	result = result_data.next()
	print result
	unicode(result)
	print type(result)
	result_dict[key] = result
	iterator = result_data.alive
	with open('app/js/tweets.json', 'w') as outfile:
		json.dump(result_dict, outfile, default=json_util.default)
	key += 1	
else:
	print 'done'

print result_dict


	# json.dumps(result_dict)
    # json.dump(result_dict, outfile, indent=4)



print 'deadbeef'

## parent: 1, author: 1, text: 1, hashtags: 1, author_name: 1, user_mentions: 1, to: 1, tweet_sentiment: 1, tweet_id: 1, _id: 1 }