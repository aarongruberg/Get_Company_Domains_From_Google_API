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
f = 'sampleList.csv'
df = pd.read_csv(f)
df = df.head(10)

#------------------------------------------------------------------------------------------------------------

def getDomain(company_name):

	query = company_name
	params = {
			'query': query,
			'limit': 1,
			'indent': True,
			'key': api_key,
	}

	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())

	if 'itemListElement' in response.keys():
		for element in response['itemListElement']:
			if 'url' in element['result'].keys():
				element['result']['url'] = element['result']['url'].encode("utf-8")
				return element['result']['url']

#-------------------------------------------------------------------------------------------------------------

# Helper function
def getDomains(accountName):

	df['Domain'] = accountName.apply(getDomain)
	return df

#-------------------------------------------------------------------------------------------------------------

# Test helper function
df = getDomains(df['Account Name'])


# What % of domains were retrieved
num_names = df['Account Name'].count()
num_domains = df['Domain'].count()
ratio = float(num_domains) / float(num_names)
percent = ratio * 100
print "'%' of domains retrieved:", round(percent, 2)


df.to_csv('sampleListInput.csv', index = False)





