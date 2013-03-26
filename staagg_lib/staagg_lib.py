'''staagg lib: Python interface to the Staagg API
'''

__version__ = '1.0'
__author__ = 'Siddharth Saha (sidchilling@gmail.com)'

import xml.etree.ElementTree as ET
import requests

class StaaggLib(object):

    BASE_URL = 'http://www.staagg.com/webservices/v4'

    key = ''

    def __init__(self, key):
	assert key, 'The Staagg API Key is required'
	self.key = key
    
    def _get_remaining_calls(self, tree):
	# This is a private method which returns the remaining calls from the tree
	return tree.find('metadata').get('remainingCalls')
    
    def _get_item_list(self, tree):
	# This function reads the item list and returns a list
	l = []
	for item in tree.find('items').findall('item'):
	    keys = item.keys()
	    item_dict = {} # dict for this particular item
	    for key in keys:
		item_dict[key] = item.get(key)
	    l.append(item_dict)
	return l
    
    def _make_return_dict(self, content, name):
	tree = ET.fromstring(content)
	return {
		'remaining_calls' : self._get_remaining_calls(tree = tree),
		name : self._get_item_list(tree = tree)
		}

    def get_networks(self):
	'''This method returns all the networks of the Staagg platform
	'''
	url = '%s/getNetworks/userWsKey/%s' %(self.BASE_URL, self.key)
	r = requests.post(url = url)
	if r.ok:
	    return self._make_return_dict(content = r.content, name = 'networks')
	else:
	    raise Exception('Cannot connect to Staagg Service')

    def get_currencies(self):
	'''This method gets all the information about all the currencies that 
	is supported by Staagg
	'''
	url = '%s/getCurrencies/userWsKey/%s' %(self.BASE_URL, self.key)
	r = requests.post(url = url)
	if r.ok:
	    return self._make_return_dict(content = r.content, name = 'currencies')
	else:
	    raise Exception('Cannot connect to Staagg Service')

    def get_network_accounts(self):
	'''Retrieves the network accounts'''
	url = '%s/getNetworkAccounts/userWsKey/%s' %(self.BASE_URL, self.key)
	r = requests.post(url = url)
	if r.ok:
	    return self._make_return_dict(content = r.content, name = 'network_accounts')
	else:
	    raise Exception('Cannot connect to Staagg Service')

    def get_user(self):
	'''Returns your user info'''
	url = '%s/getUser/userWsKey/%s' %(self.BASE_URL, self.key)
	r = requests.post(url = url)
	if r.ok:
	    return self._make_return_dict(content = r.content, name = 'user')
	else:
	    raise Exception('Cannot connect to Staagg Service')

    def get_transactions(self, start_date, end_date, date_type, network_account_id, page = 1):
	'''This methods gets the transactions - See Staagg Documentation 
	for complete documentation'''
	url = '%s/getTransactions/userWsKey/%s/startDateTime/%s/endDateTime/%s/dateType/%s/networkAccId/%s/page/%s' \
		%(self.BASE_URL, self.key, start_date.strftime('%Y-%m-%dT%H:%M:%S'),
			end_date.strftime('%Y-%m-%dT%H:%M:%S'),
			date_type, network_account_id, page)
	r = requests.post(url = url)
	if r.ok:
	    return self._make_detailed_return_dict(content = r.content, name = 'transactions')
	else:
	    raise Exception('Cannot connect to Staagg Service')
    
    def _make_detailed_return_dict(self, content, name):
	# This method makes a more detailed return dict for get_transactions and get_clicks
	res = self._make_return_dict(content = content, name = name)
	tree = ET.fromstring(content)
	res['page'] = tree.find('metadata').get('page')
	res['total_pages'] = tree.find('metadata').get('totalPages')
	res['page_items'] = tree.find('metadata').get('pageItems')
	res['total_items'] = tree.find('metadata').get('totalItems')
	return res

    def get_clicks(self, start_date, end_date, network_account_id, page = 1):
	'''This method gets the clicks info - Full documentation on the 
	Staagg Documentation'''
	url = '%s/getClicks/userWsKey/%s/startDateTime/%s/endDateTime/%s/networkAccId/%s/page/%s' \
		%(self.BASE_URL, self.key, start_date.strftime('%Y-%m-%dT%H:%M:%S'),
			end_date.strftime('%Y-%m-%dT%H:%M:%S'),
			network_account_id, page)
	r = requests.post(url = url)
	if r.ok:
	    return self._make_detailed_return_dict(content = r.content, name = 'clicks')
	else:
	    raise Exception('Cannot connect to Staagg Service')
