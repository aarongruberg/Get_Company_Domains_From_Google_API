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

text = ['inc', 'Inc', 'INC', 'llc', 'Llc', 'LLC']

#------------------------------------------------------------------------------------------------------------

# Need to check that text is the last word in the string before removal

def removeText(company_name):

	#company_name = company_name.split(' ')
	last = company_name[-1]

	for item in text:
		if item == last:
			company_name = company_name[:-1]
			company_name = ' '.join(company_name)

	return company_name

#------------------------------------------------------------------------------------------------------------

def getDomain(company_name):

	count = 0

	# First query

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
				count += 1
				element['result']['url'] = element['result']['url'].encode("utf-8")
				return element['result']['url']


	# Conditional second query

	if count == 0:

		company_name = company_name.split(' ')
		last = company_name[-1]

		if last in text:
			query = removeText(company_name)

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
						count += 1
						element['result']['url'] = element['result']['url'].encode("utf-8")
						return element['result']['url']



#-------------------------------------------------------------------------------------------------------------

# Apply function
def getDomains(accountName):

	df['Domain'] = accountName.apply(getDomain)
	return df

#-------------------------------------------------------------------------------------------------------------

# Main Function
df = getDomains(df['Account Name'])


# What % of domains were retrieved
num_names = df['Account Name'].count()
num_domains = df['Domain'].count()
ratio = float(num_domains) / float(num_names)
percent = ratio * 100
print "'%' of domains retrieved:", round(percent, 2)


df.to_csv('sampleListInputGoogle.csv', index = False)



# ### TEST INDIVIDUAL QUERIES
# query = 'SIERRA PACIFIC INDUSTRIES'
# 		#print query
# params = {
# 		'query': query,
# 		'limit': 1,
# 		'indent': True,
# 		'key': api_key,
# }

# url = service_url + '?' + urllib.urlencode(params)
# response = json.loads(urllib.urlopen(url).read())

# count = 0

# if 'itemListElement' in response.keys():
# 	for element in response['itemListElement']:
# 		if 'url' in element['result'].keys():
# 			count += 1
# 			element['result']['url'] = element['result']['url'].encode("utf-8")
# 			print element['result']['url']


# if count == 0:
# 	query = query.split(' ')
# 	query = query[:-1]
# 	query = ' '.join(query)

# 	params = {
# 			'query': query,
# 			'limit': 1,
# 			'indent': True,
# 			'key': api_key,
# 	}

# 	url = service_url + '?' + urllib.urlencode(params)
# 	response = json.loads(urllib.urlopen(url).read())


# 	if 'itemListElement' in response.keys():
# 		for element in response['itemListElement']:
# 			if 'url' in element['result'].keys():
# 				count += 1
# 				element['result']['url'] = element['result']['url'].encode("utf-8")
# 				print element['result']['url']



