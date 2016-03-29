import pytest, urlparse, json, os, oauth2, base64
# from restkit import *
from user_keys import UserKeys
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

#use this decorator to declare depency injections
@pytest.fixture(scope='session') #scope tells fixture should be cached for the entire session.
def webdriver(request): #fxn name to be inputed to test. 'request' is a special fixture object
	driver = Chrome("/Users/darrickchung/Downloads/chromedriver")
	request.addfinalizer(driver.quit)
	return driver #must return object to aid test

#OAuth Authentication for a user to make API calls
@pytest.fixture(scope='function')
def auth1():
	user = UserKeys().user1()
	consumer = oauth2.Consumer(key=user["CONSUMER_KEY"], secret=user["CONSUMER_SECRET"])
	access_token = oauth2.Token(key=user["ACCESS_KEY"], secret=user["ACCESS_SECRET"])
	client = oauth2.Client(consumer, access_token)

	return client

# OAuth Authentication for a second user
@pytest.fixture(scope='function')
def auth2():
	user = UserKeys().user2()
	consumer = oauth2.Consumer(key=user["CONSUMER_KEY"], secret=user["CONSUMER_SECRET"])
	access_token = oauth2.Token(key=user["ACCESS_KEY"], secret=user["ACCESS_SECRET"])
	client = oauth2.Client(consumer, access_token)
	return client

# Posts a new tweet. Takes OAuth obj, and message str
@pytest.fixture(scope='function')
def create():
	def create_status(client, message, **kwargs):
		endpoint = "https://api.twitter.com/1.1/statuses/update.json?status=" + message
		# concatenate additional params to url
		for params in kwargs:
			endpoint += ("&" + str(params) + "=" + kwargs[params])
		
		response, data = client.request(endpoint,"POST")
		return json.loads(data)
	return create_status

# Destroys a tweet. Takes OAuth obj, and tweet_id
@pytest.fixture(scope='function')
def destroy():
	def destroy_status(client, tweet_id, **kwargs):
		endpoint = "https://api.twitter.com/1.1/statuses/destroy/"+tweet_id+".json?"
		for params in kwargs:
			endpoint += ("&" + str(params) + "=" + kwargs[params])
		response, data = client.request(endpoint,"POST")
		return json.loads(data)
	return destroy_status

@pytest.mark.statuses
def test_user_timeline(auth1):
	endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json"
	response, data = auth1.request(endpoint)
	tweets = json.loads(data)

	assert not "errors" in tweets, "Expected to get all user tweets"

@pytest.mark.statuses
def test_post_new_status(auth1,create,destroy):
	data = create(auth1, "Hello%20World")
	destroy(auth1,data["id_str"])

	assert not "errors" in data  
	assert data["text"] == "Hello World", "Expected Hello World message in 'text' key"

@pytest.mark.statuses
def test_post_new_status_char_limit(auth1,create,destroy):
	tweet = "ilovechickenilovechickenilovechickenilovechickenilovechickenilovechickenilovechickenilovechickenilovechickenilovechickenilovechickenilovechickenilovechickenilovechickenilovechickenilovechickenilovechicken"
	data = create(auth1, tweet)

	assert "errors" in data 
	assert data["errors"][0]['message'] == "Status is over 140 characters." 

@pytest.mark.statuses
def test_post_new_status_long_not_provided(auth1,create,destroy):
	data = create(auth1, "Hello%20World", lat = "10")
	assert "errors" in data, "Expected errors"
	assert data["errors"][0]["message"] == 'Invalid coordinates.', "Expected error msg"

@pytest.mark.statuses
def test_post_new_status_lat_not_provided(auth1,create,destroy):
	data = create(auth1, "Hello%20World", long = "10")

	assert "errors" in data, "Expected errors"
	assert data["errors"][0]["message"] == 'Invalid coordinates.', "Expected error msg"

@pytest.mark.statuses
def test_post_new_status_lat_out_of_range(auth1,create,destroy):
	data = create(auth1, "Hello%20World", lat = "200")
	if not "errors" in data:
		destroy(auth1,data["id_str"])

	assert "errors" in data, "Expected errors"
	assert data["errors"][0]["message"] == 'Invalid coordinates.', "Expected error msg"

@pytest.mark.statuses
def test_post_new_status_lng_out_of_range(auth1,create,destroy):
	data = create(auth1, "Hello%20World", long = "200")
	if not "errors" in data:
		destroy(auth1,data["id_str"])

	assert "errors" in data, "Expected errors"
	assert data["errors"][0]["message"] == 'Invalid coordinates.', "Expected error msg"

@pytest.mark.statuses
def test_destroy_status(auth1, create, destroy):
	new_status = create(auth1, "Hello%20World")
	data = destroy(auth1,new_status["id_str"])

	assert not "errors" in data 
	assert data["id_str"] == new_status["id_str"], "Expected no errors and for 'id_str' value to match"

@pytest.mark.statuses
def test_destroy_status_params_trim_user(auth1, create, destroy):
	new_status = create(auth1, "Hello%20World")
	data = destroy(auth1,new_status["id_str"],trim_user="true")

	assert not "errors" in data
	assert len(data["user"]) <= 2, "Expected user key to only have 2 values"

@pytest.mark.statuses
def test_retweet(auth1, auth2, create, destroy):
	new_status1 = create(auth1, "Hello%20World")# create new status tweet 
	endpoint = "https://api.twitter.com/1.1/statuses/retweet/"+new_status1["id_str"]+".json"
	response, data = auth2.request(endpoint,"POST")#use the status_id and auth2 to retweet status
	data = json.loads(data)
	destroy(auth1,new_status1["id_str"])# Destroying orig tweet will destroy retweet too

	assert new_status1["id_str"] == data["retweeted_status"]["id_str"], "Expected id_str of original tweet to equal id_str of retweet" 
	
@pytest.mark.statuses
def test_undo_retweet(auth1,auth2,create,destroy):
	# create new status tweet 
	new_status1 = create(auth1, "Hello%20World")
	# retweet with second user
	retweet_endpoint = "https://api.twitter.com/1.1/statuses/retweet/"+new_status1["id_str"]+".json"
	response, data = auth2.request(retweet_endpoint,"POST")
	id_str = json.loads(data)["retweeted_status"]["id_str"]
	# send unretweet call
	unretweet_endpoint = "https://api.twitter.com/1.1/statuses/unretweet/"+id_str+".json"
	response2, data2 = auth2.request(unretweet_endpoint,"POST")
	unretweet_id_str = json.loads(data2)["id_str"]
	
	destroy(auth1,new_status1["id_str"])

	assert id_str == unretweet_id_str, "Expected retweet's id_str to equal unretweet's id_str"





