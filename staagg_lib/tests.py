# This is a file for hand-written tests for the Staagg Python library

from staagg_lib import StaaggLib
from pprint import pprint

if __name__ == '__main__':
    api_key = '<YOUR_API_KEY>'
    staagg = StaaggLib(key = api_key) # This is the staagg object

    # Getting all the networks
    pprint(staagg.get_networks())

    # Getting all the currencies
    pprint(staagg.get_currencies())

    # Getting all network accounts
    pprint(staagg.get_network_accounts())

    # Getting the user
    pprint(staagg.get_user())

    # Getting transactions
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    to_date = datetime.utcnow() + relativedelta(days = -1)
    from_date = to_date + relativedelta(days = -7)
    to_date = datetime.strptime('%s 23:59:59' %(to_date.strftime('%Y-%m-%d')), 
	    '%Y-%m-%d %H:%M:%S')
    from_date = datetime.strptime('%s 00:00:00' %(from_date.strftime('%Y-%m-%d')), 
	    '%Y-%m-%d %H:%M:%S')
    print 'from_date: %s' %(from_date.strftime('%Y-%m-%dT%H:%M:S'))
    print 'to_date: %s' %(to_date.strftime('%Y-%m-%dT%H:%M:%S'))
    print(staagg.get_transactions(start_date = from_date, end_date = to_date, 
	date_type = 'transactionDate', network_account_id = 958, page = 1))

    print(staagg.get_transactions(start_date = from_date, end_date = to_date, 
	date_type = 'validationDate', network_account_id = 958))

    # Getting the clicks
    print(staagg.get_clicks(start_date = from_date, end_date = to_date, 
	network_account_id = 958))
    
