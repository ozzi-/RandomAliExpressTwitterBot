# Get geckodriver -> https://github.com/mozilla/geckodriver/releases
import requests, random, tweepy as tw
from selenium import webdriver
from time import sleep
from urllib.parse import urljoin, urlprase
from creds import *

def getWords():
	word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

	response = requests.get(word_site)
	WORDS = response.content.splitlines()
	word1 = str(random.choice(WORDS).decode())
	word2 = str(random.choice (WORDS).decode())
	return word1+"+"+word2

def doSearch(browser,searchText):
	print("searching for "+searchText)
	browser.get('https://www.aliexpress.com/wholesale?SearchText='+searchText)
	elem = browser.find_element_by_xpath("//*")
	return elem.get_attribute("outerHTML")

def getFirstItemHref(browser):
	elems = browser.find_elements_by_xpath("//a[@href]")
	for elem in elems:
		href = elem.get_attribute("href")
		if "www.aliexpress.com/item/" in href:
			return href

def screenShotItem(browser,url):
	scPath = "screenshot.png";
	browser.get(url)
	browser.get_screenshot_as_file(scPath)
	return scPath

def tweetWithImage(text,mediaPath):
	auth = tw.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tw.API(auth, wait_on_rate_limit=True)
	sleep(1)
	browser.quit()
	api.update_status_with_media(text,mediaPath)


searchText = getWords()
browser = webdriver.Firefox()
responseBody = doSearch(browser,searchText)

while "Sorry, your search \"" in responseBody:
	searchText = getWords()
	responseBody = doSearch(browser,searchText)

# https://www.aliexpress.com/item/4000288191878.html?algo_pvid=d7a0a9a4-86b4-4d5e-b1c1-f024ebb3a6e3&algo_exp_id=d7a0a9a4-86b4-4d5e-b1c1-f024ebb3a6e3-0&pdp_ext_f=%7B%22sku_id%22%3A%2210000014022551024%22%7D
href=getFirstItemHref(browser)
href=urljoin(href, urlparse(href).path) 
scPath=screenShotItem(browser,href)
tweetWithImage("\""+searchText.replace("+"," ")+"\"",scPath)
quit()