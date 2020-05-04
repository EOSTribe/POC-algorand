import requests
import pprint
import os

upstream = os.environ.get('UPSTREAM_API',"http://algo-ua.eostribe.io")

def getLastRound():
    response = requests.get(upstream+'/v1/status')
    if response.status_code == 200:
        r = response.json()
        return r['lastRound']


def getTransactions(lastRound):
    lastRound = 6476693
    response = requests.get(upstream+'/v1/block/'+str(lastRound))
    if response.status_code == 200:
        r = response.json()
        transactions = []


getTransactions(getLastRound())


