# API-BCA
##sandboxed API for BCA (Bank Central Asia)

fill out your credentials first from developer.bca.co.id inside ==settings.py== file

###usage

`$git clone https://github.com/zahris85/Python-API-BCA.git`

`$cd Python-API-BCA`

`$python`

`>>> import client as bca`

####print accounts balance

`>>> bca.print_balance()`

####print account statements`

the sandbox only give specific date of data

`>>> bca.print_statements()`

####fund transfer :

this method need 4 params ({trans amount}, {recipient}, {first remark}, {second remark})

transfer funds recipient 0201245681 for a success transaction

just set remarks on blanks if you don't want to input it

`>>> bca.transfer('10000.00', '0201245681' ,'', '')`
