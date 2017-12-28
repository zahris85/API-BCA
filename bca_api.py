import requests, datetime, hashlib, hmac, json
from base64 import b64encode
from settings import *


class BCA_API:

    ## generate token
    def get_access_token(self):

        string = client_id + ':' + client_secret

        auth = b64encode(string.encode()).decode()

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + auth
        }

        data = 'grant_type=client_credentials'

        r = requests.post(host + '/api/oauth/token', headers=headers, data=data)

        return r.json()['access_token']

    # generate signature
    def get_signature(self, method, path, access_token, timestamp, request_body=''):

        secret = api_secret.encode()

        request_body_hash = hashlib.sha256(
            request_body.encode()
        ).hexdigest().lower()

        StringToSign = (
            method + ':' +
            path + ':' +
            access_token + ':' +
            request_body_hash + ':' +
            timestamp
        ).encode()

        signature = hmac.new(secret, StringToSign, digestmod=hashlib.sha256)

        return signature.hexdigest().encode()

    # generate current timestamp
    def get_timestamp(self):

        return datetime.datetime.now().isoformat()[:-3] + '+07:00'

    # get accounts balance
    def get_balance(self, **val):

        path = '/banking/v3/corporates/' + corporate_id + \
               '/accounts/' + '%2C'.join(x for x in account_numbers)

        timestamp = self.get_timestamp()

        signature = self.get_signature(
            'GET', path, val['tkn'], timestamp
        )

        header = {
            "Authorization": "Bearer " + val['tkn'],
            "Content-Type": "application/json",
            "Origin": origin,
            "X-BCA-Key": api_key,
            "X-BCA-Timestamp": timestamp,
            "X-BCA-Signature": signature
        }

        r = requests.get(host + path, headers=header)

        return r.content.decode()

    # get account statements
    def get_statements(self, **val):

        path = '/banking/v3/corporates/' + corporate_id + \
               '/accounts/' + account_numbers[0] + \
               '/statements?EndDate=' + val['end'] +\
               '&StartDate=' + val['str']

        timestamp = self.get_timestamp()

        signature = self.get_signature('GET', path, val['tkn'], timestamp)

        header = {
            "Authorization": "Bearer " + val['tkn'],
            "Content-Type": "application/json",
            "Origin": origin,
            "X-BCA-Key": api_key,
            "X-BCA-Timestamp": timestamp,
            "X-BCA-Signature": signature
        }

        r = requests.get(host + path, headers=header)

        return r.content.decode()

    # transfer funds
    def transfer(self, **val):

        path = '/banking/corporates/transfers'

        timestamp = self.get_timestamp()

        request_body = {
            "CorporateID" : corporate_id,
            "SourceAccountNumber" : val['src'],
            "TransactionID" : val['tid'],
            "TransactionDate" : timestamp[:10],
            "ReferenceID" : val['rid'],
            "CurrencyCode" : "IDR",
            "Amount" : val['amt'],
            "BeneficiaryAccountNumber" : val['rcp']
        }

        request_body.update(val['rmk'])

        data = json.dumps(request_body, separators=(',', ':'))

        signature = self.get_signature('POST', path, val['tkn'], timestamp, data)

        headers = {
            "Authorization" : "Bearer " + val['tkn'],
            "Content-Type" : "application/json",
            "Origin" : origin,
            "X-BCA-Key" : api_key,
            "X-BCA-Timestamp" : timestamp,
            "X-BCA-Signature" : signature
        }

        r = requests.post(host + path, headers=headers, data=data)

        return r.content.decode()
