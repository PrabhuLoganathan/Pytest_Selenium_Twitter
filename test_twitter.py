import pytest, oauth2, urlparse, json, os
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

@pytest.fixture(scope='function')
def oauth(webdriver):

	CONSUMER_KEY = os.environ["CONSUMER_KEY"]
	CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
	ACCESS_KEY = os.environ["ACCESS_KEY"]
	ACCESS_SECRET = os.environ["ACCESS_SECRET"]

	consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth2.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth2.Client(consumer, access_token)

	return client


def test_website_title(webdriver):
	webdriver.get('https://dev.twitter.com/rest/tools/console')
	assert 'API Console Tool | Twitter Developers' in webdriver.title


def test_login(webdriver): 
	# Navigate to login page
	webdriver.get('https://twitter.com/login')
	# Enter login info & submit
	webdriver.find_element_by_class_name('js-username-field').send_keys('gideon1990@gmail.com')
	webdriver.find_element_by_class_name('js-password-field').send_keys('gideoniscool')
	webdriver.find_element_by_class_name("js-signin").submit()
	
	# Wait for DOM to load profile information
	profileInfo = WebDriverWait(webdriver,10).until(
		EC.presence_of_element_located((By.CLASS_NAME, "DashboardProfileCard-content"))
	)

	assert profileInfo != None

def test_api(oauth,webdriver):

	timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json"
	response, data = oauth.request(timeline_endpoint)

	tweets = json.loads(data)
	print tweets
	for tweet in tweets:
	    print tweet['text']












