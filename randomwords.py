# 0. https://developer.twitter.com/en/apply-for-access & apply for account
# 1.	Create App
# 2.	Make sure App permission is set to "Read and Write"
# 3.	Create creds and save as creds.py
# 4.	Get chromiumdriver binary and place in a path where python will find it
#		https://sites.google.com/chromium.org/driver/

import requests, random, tweepy as tw
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from creds import *

aliExpressBaseSearchURL='https://www.aliexpress.com/wholesale?SearchText='
aliExpressItemHrefMarker='aliexpress.com/item/'
sorryNotFoundMarker="Sorry, your search \""
WINDOW_SIZE = "1280,1000"
chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

def getWords():
	word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
	response = requests.get(word_site)
	WORDS = response.content.splitlines()
	word1 = str(random.choice(WORDS).decode ())
	word2 = str(random.choice(WORDS).decode())
	return word1+"+"+word2

def doSearch(browser,searchText):
	print("searching for "+searchText)
	browser.get(aliExpressBaseSearchURL+searchText)
	elem = browser.find_element_by_xpath("//*")
	return elem.get_attribute("outerHTML")

def getFirstItemHref(browser):
	elems = browser.find_elements_by_xpath("//a[@href]")
	for elem in elems:
		href = elem.get_attribute("href")
		if aliExpressItemHrefMarker in href:
			return href
	raise Exception("Could not find any hrefs starting with /item - my guess its DNS :^)")

def screenShotItem(browser,url):
	scPath = "screenshot.png";
	browser.get(url)
	browser.implicitly_wait(3)
	browser.find_element_by_xpath("//button[@data-role='gdpr-accept']").click()
	browser.get_screenshot_as_file(scPath)
	return scPath

def tweetWithImage(text,mediaPath):
	auth = tw.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tw.API(auth, wait_on_rate_limit=True)
	sleep(1)
	api.update_status_with_media(text,mediaPath)
	print("Tweeted "+text)

searchText = getWords()
browser = webdriver.Chrome(chrome_options=chrome_options)
responseBody = doSearch(browser,searchText)

while sorryNotFoundMarker in responseBody:
	searchText = getWords()
	responseBody = doSearch(browser,searchText)

href=getFirstItemHref(browser)
href=urljoin(href, urlparse(href).path) 
scPath=screenShotItem(browser,href)
tweetWithImage("\""+searchText.replace("+"," ")+"\"",scPath)
browser.quit()
quit()
