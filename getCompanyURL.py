### GET COMPANY DOMAIN FROM GOOGLE API

### This script makes queries to Google's Knowledge Graph Search API 
### Queries are made with a company name and the company's domain is retrieved.
### The goal is to read a list match input file and add domains before it is 
### imported to the platform.

import json
import urllib
import pandas as pd 

api_key = 'AIzaSyCTVEnopRQIgUkS0BunQ3pQFq64FnYP2O4'
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'

# Read input list file
f = 'EastRegionACQ_top100.csv'
df = pd.read_csv(f)
#df = df.head(13)

#-------------------------------------------------------------------------------------------------------------

def getAPI_Name(name):

	query = name
	params = {
			'query': query,
			'limit': 1,
			'indent': True,
			'key': api_key,
	}

	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())

	for element in response['itemListElement']:
		if 'name' in element['result'].keys():
			element['result']['name'] = element['result']['name'].encode("utf-8")
			return element['result']['name']


# Call getAPI_Name() on a dataframe column using .apply()
# Planning to vectorize pandas series to speed up runtime.
df['API_names'] = df['Account Name'].apply(getAPI_Name)

#------------------------------------------------------------------------------------------------------------

def getAPI_Domain(api_name):

	query = api_name
	params = {
			'query': query,
			'limit': 1,
			'indent': True,
			'key': api_key,
	}

	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())

	for element in response['itemListElement']:
		if 'url' in element['result'].keys():
			if element['result']['name'] == query:
				element['result']['url'] = element['result']['url'].encode("utf-8")
				return element['result']['url']


df['Domain'] = df['API_names'].apply(getAPI_Domain)
df = df.drop(['API_names'], axis = 1)

# What % of domains were retrieved
num_names = df['Account Name'].count()
num_domains = df['Domain'].count()
ratio = float(num_domains) / float(num_names)
percent = ratio * 100
print "'%' of domains retrieved:", round(percent, 2)


df.to_csv('EastRegionACQ_top100_input.csv', index = False)











