#demo for BCA API using sandbox

import json
from bca_api import BCA_API

bca = BCA_API() # creating alias, easier to remember

### generate access token
try :
    token = bca.get_access_token()
except KeyError :
    print("please input your credentials first inside settings.py")

### get current accounts balance
def print_balance():
    r = bca.get_balance(tkn=token)
    data = json.loads(r)

    print("\n================\nACCOUNTS BALANCE\n================")

    # iterate balance for each account
    [ print('Account Num : ' + x['AccountNumber'] + ' ---> ' + 'Balance : Rp.' + x['Balance'])
      for x in data['AccountDetailDataSuccess'] ]

    # display all invalid accounts
    print("\nthis accounts are invalid = {} ".format(
        ", ".join(x['AccountNumber'] for x in data['AccountDetailDataFailed'])))


### get statements for specific range of date
def print_statements():

    start_date = '2016-08-29'

    end_date = '2016-08-30'

    print("\n==============="
          "\nSTATEMENTS"
          "\nFROM " + start_date +
          "\nTILL " + end_date +
          "\n===============\n")

    r = bca.get_statements(tkn=token, str=start_date, end=end_date)
    data = json.loads(r)

    #iterate all 'D' or Debit transactions
    print("Debit Transactions :\n\n===============\n")
    for i in data['Data']:
        [print('{} : {}'.format(key, val)) for key, val in i.items() if i['TransactionType'] == 'D']
        print('\n===============\n')  if i['TransactionType'] == 'D' else None

    # iterate all 'C' or Credit transactions
    print("Credit Transactions :\n===============\n")
    for i in data['Data']:
        [print('{} : {}'.format(key, val)) for key, val in i.items() if i['TransactionType'] == 'C']
        print('\n===============\n')  if i['TransactionType'] == 'C' else None


### transfer funds recipient 0201245681 for success,  0201245501 for closed account
def transfer(amt, rcp, *rmk):

    source = "0201245680"

    trans_id = "0088"

    ref_id = "888/344/bb8"

    remarks = {}

    try:
        [ remarks.update({'Remark' + str(x + 1): rmk[x]}) for x in range(2) ]
        r = bca.transfer(tkn=token, src=source, rcp=rcp, rmk=remarks, amt=amt, tid=trans_id, rid=ref_id)
        transfer = json.loads(r)
        print(transfer['Status'])
    except IndexError:
        print("please put at least 2 remarks")
        print('format = print_transfer("value", "remark1", "remark2")')
    except KeyError:
        print("account invalid use 0201245681 for demo")
