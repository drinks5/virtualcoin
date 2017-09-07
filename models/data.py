# encoding: utf-8
from time import sleep
from pymongo import UpdateOne
import requests
import pymongo
client = pymongo.MongoClient("localhost", 27017)

db = client.virtualcoin

collection = db.vc


def getter(url):
    return requests.get(url).json()


class BtcTrade(object):
    def __init__(self, coin='eth', step=300, hooks=None):
        self.coin = coin
        self.url = 'https://plugin.sosobtc.com/'
        self.step = step
        self.hooks = hooks or []
        if not isinstance(self.hooks, list):
            self.hooks = [self.hooks]

    def period(self, step=None):
        path = 'widgetembed/data/period?symbol=btctrade{}cny&step={}'.format(
            self.coin, step or self.step)
        return getter(self.url + path)

    def init(self):
        for step in (60, 300, 600, 900, 1800, 3600, 86400):
            self.bulk(step)

    def bulk(self, step):
        response = self.period(step)
        # open high low close vol
        keys = ['open', 'high', 'low', 'close', 'vol']
        dataset = [
            UpdateOne(
                {
                    'timestamp': x[0]
                }, {"$set": dict(zip(keys, x[1:]))},
                upsert=True) for x in response
        ]
        result = collection.bulk_write(dataset)
        print(result.bulk_api_result)
        print(collection.count())

    def forever(self):
        while True:
            self.bulk(60)
            sleep(30)


if __name__ == '__main__':
    BtcTrade().forever()
