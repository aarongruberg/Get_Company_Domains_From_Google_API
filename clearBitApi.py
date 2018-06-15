### GET COMPANY DOMAIN FROM CLEARBIT AUTOCOMPLETE API

# This script checks company names in a csv for terms like 'inc' or 'llc'
# before calling the api for company domains.

import json
import urllib
import pandas as pd 


# I didn't need a key for the autocomplete api
#clearbit.key = 'sk_0f12e5f43a4c7bf91ffa11890982588c'

service_url = 'https://autocomplete.clearbit.com/v1/companies/suggest?'

# Read input list file
f = 'sampleList.csv'
df = pd.read_csv(f)
df = df.head(10)

#------------------------------------------------------------------------------------------------------------

# Need to check that text is the last word in the string before removal

def removeText(company_name):

	text = ['inc', 'Inc', 'INC', 'llc', 'Llc', 'LLC']

	#company_name = company_name.split(' ')
	last = company_name[-1]

	for item in text:
		if item == last:
			company_name = company_name[:-1]
			company_name = ' '.join(company_name)

	return company_name

#------------------------------------------------------------------------------------------------------------

def getDomain(company_name):

	text = ['inc', 'Inc', 'INC', 'llc', 'Llc', 'LLC']
	company_name = company_name.split(' ')
	last = company_name[-1]

	if last in text:
		query = removeText(company_name)
		#print query

	else:
		query = company_name
		#print query

	params = {
			'query': query
	}

	url = service_url + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())

	if len(response) > 0:
		return response[0]['domain']

#print getDomain(name)

#-------------------------------------------------------------------------------------------------------------

# Helper function
def getDomains(accountName):

	df['Domain'] = accountName.apply(getDomain)
	return df

#-------------------------------------------------------------------------------------------------------------

df = getDomains(df['Account Name'])

# What % of domains were retrieved
num_names = df['Account Name'].count()
num_domains = df['Domain'].count()
ratio = float(num_domains) / float(num_names)
percent = ratio * 100
print "'%' of domains retrieved:", round(percent, 2)


df.to_csv('sampleListInputClearBit.csv', index = False)


### TESTING THIS FUNCTION
#print removeText('BLUE CROSS AND BLUE SHIELD OF FLORIDA INC')





