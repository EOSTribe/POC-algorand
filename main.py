import requests
from pprint import pprint
import os
import json
import redis
import time
import schedule


upstream = os.environ.get('UPSTREAM_API',"http://algo.eostribe.io")
redis_host = os.environ.get('REDIS_HOST',"localhost")

redis_client = redis.Redis(host=redis_host, port=6379, db=0)
latest_proceeded_round = 0
nextConsensusVersionRound = 0

def getLastRound():
    global latest_proceeded_round
    global nextConsensusVersionRound
    response = requests.get(upstream+'/v1/status')
    if response.status_code == 200:
        r = response.json()
        lastRound = r['lastRound']
        nextConsensusVersionRound=r['nextConsensusVersionRound']
        if latest_proceeded_round == 0:
            latest_proceeded_round = lastRound
            return lastRound
        else:
            if lastRound - latest_proceeded_round == 1:
                latest_proceeded_round = lastRound
                return lastRound
            else:
                print()
                print("lastRound - latest_proceeded_round: "+str(lastRound - latest_proceeded_round))
                latest_proceeded_round = lastRound
                time.sleep(1)
                return latest_proceeded_round

def getTransactions(lastRound):
    response = requests.get(upstream+'/v1/block/'+str(lastRound))
    if response.status_code == 200:
        r = response.json()
        transactions = r['txns']
        print(lastRound)
        pprint(transactions)
        return transactions


def job():
    txs = getTransactions(getLastRound())
    if txs is not None:
        if len(txs) >0:
            redis_client.publish('algo_txs', json.dumps(txs))

schedule.every(4).seconds.do(job)


while 1:
    schedule.run_pending()



