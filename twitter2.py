import oauth2 as oauth
import json

CONSUMER_KEY = "consumerkey"
CONSUMER_SECRET = "consumersecret"
ACCESS_KEY = "accesskey"
ACCESS_SECRET = "accesssecret"

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json"
response, data = client.request(timeline_endpoint)

tweets = json.loads(data)
for tweet in tweets:
    print tweet['text']

print client


# @pytest.fixture(scope='session')
# def oauth(webdriver):
# 	# Create your consumer with the proper key/secret.
# 	consumer = oauth2.Consumer(key="consumerkey", secret="secretkey")
 
# 	# Request token URL for Twitter.
# 	request_token_url = "https://api.twitter.com/oauth/request_token"
# 	access_token_url = 'https://api.twitter.com/oauth/access_token'
# 	authorize_url = 'https://api.twitter.com/oauth/authorize'

# 	# Create our client.
# 	client = oauth2.Client(consumer)


# 	# The OAuth Client request works just like httplib2 for the most part.
# 	resp, content = client.request(request_token_url, "GET")
# 	if resp['status'] != '200':
# 	    raise Exception("Invalid response %s." % resp['status'])

# 	request_token = dict(urlparse.parse_qsl(content))
# 	# print response
# 	return request_token