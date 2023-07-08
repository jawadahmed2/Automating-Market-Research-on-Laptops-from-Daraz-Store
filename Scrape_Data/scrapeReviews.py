#import required libraries For Scraping and wordclouding
from typing import final
import requests
from bs4 import BeautifulSoup # For web scraping purpose
import pandas as pd
import json
import numpy as np
from os import path # The OS module in Python provides functions for interacting with the operating system for example os.path, etc.
#from PIL import Image #PIL is python imaging library
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
# import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


# Following are adding the headers that are giving information about the resource to be fetched,
# or about the client requesting the resource
HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)  Chrome/90.0.4430.212 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

# Below function will be used to scrape data
def getdata(url):
    r = requests.get(url, headers=HEADERS)
    return r.text

def getTitle(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.content, "lxml")
    # Outer Tag Object
    title = soup.find("span", attrs={"id":'productTitle'})
    # Inner NavigableString Object
    title_value = title.string
    title_value = title_value.split()
    return ' '.join(title_value[:3])

# Below code is used to parse the html code
def parse_html(url):
    htmldata = getdata(url)
    return BeautifulSoup(htmldata, 'html.parser')

# finding html tag and converting to strings in order to get the customer names
def get_cus_names(soup):
	data_str = ""
	cus_list = []
	for item in soup.find_all("span", class_="a-profile-name"):
		data_str = data_str + item.get_text()
		cus_list.append(data_str)
		data_str = ""
	return cus_list

# find the Html tag and convert into strings in order to get the customers reviews
def get_cus_reviews(soup):
    data_str = ""
    for item in soup.find_all("div", class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content"):
      data_str = data_str + item.get_text()
    result = data_str.split("\n")
    return [i for i in result if i != ""]

# save customers name and the its review as pandas dataframe
def reviews_in_json(name, rev, title):
  data = {'Name': name, 'Review': rev, 'Title': title}
  return json.dumps(data)

# save customers name and the its review as pandas dataframe
def make_dataframe(name, rev):
    data = {'Name': name, 'Review': rev}
    return pd.DataFrame(data)

def wordCloud(df):
    get_reviews = df.Review
    text = " ".join(get_reviews)
    print(f"There are {len(text)} words in the combination of all review.")
    # Create stopword list:
    stop = set(stopwords.words('english'))
    stop.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '@', '#', 'rt', 'amp', 'http', 'https', '/', '://', '_', 'co'])
    reviews_str = get_reviews.str.cat(sep = ' ')
    list_of_words = [i.lower() for i in wordpunct_tokenize(reviews_str) if i.lower() not in stop and i.isalpha()]
    wordfreqdist = nltk.FreqDist(list_of_words)
    list_of_tuples = wordfreqdist.most_common(15)
    return [tuple[0] for tuple in list_of_tuples]