from pymongo import UpdateOne
import json
import requests
from datetime import datetime
import pandas as pd
import pymongo
from stockstats import StockDataFrame

from sanic import Sanic

app = Sanic(__name__)

client = pymongo.MongoClient("localhost", 27017)

db = client.virtualcoin

collection = db.vc

# result = collection.create_index([('timestamp', pymongo.ASCENDING)], unique=True)

formatmap = {"hourly": "%H:%M",
             'daily': '%Y-%m-%d %H:%M'}
keys = ['date', 'amount', 'close', 'high', 'low', 'open', 'volume']

def getter(url):
    return requests.get(url).json()

class BtcTrade(object):
    def __init__(self, coin, step=300):
        self.coin = coin
        self.url = 'https://plugin.sosobtc.com/'
        self.step = step

    def period(self, step=None):
        path = 'widgetembed/data/period?symbol=btctrade{}cny&step={}'.format(self.coin, step or self.step)
        return getter(self.url + path)

    def init(self):
        for step in (60, 300, 600, 900, 1800, 3600, 86400):
            self.bulk(step)

    def bulk(self, step):
        response = self.period(step)
        # open high low close vol
        keys = ['open', 'high', 'low', 'close', 'vol']
        dataset = [UpdateOne({'timestamp': x[0]}, {"$set": dict(zip(keys, x[1:]))}, upsert=True) for x in response]
        result = collection.bulk_write(dataset)
        print(result.bulk_api_result)
        print(collection.count())


@app.websocket('/feed')
async def feed(request, ws):
    format = 'daily'
    query = {}
    querystring = ''
    while True:
        querystring.isdigit() and query.update(timestamp={"$gt": int(querystring)})
        response = collection.find(query)
        dates = (x['timestamp'] for x in response)
        dates = [datetime.fromtimestamp(x).strftime(formatmap[format]) for x in dates]
        dataset = [x['data'] for x in response]
        await ws.send(json.dumps(dict(dates=dates, dataset=dataset)))
        querystring = await ws.recv()

def calc():
    df = pd.DataFrame.from_records(collection.find().sort('timestamp', -1))
    del df['_id']
    df['amount'] = df['close'] * df['vol']
    renamemap = {'vol': 'volume'}
    df.columns = [renamemap.get(x, x) for x in df.columns]
    ticker = StockDataFrame.retype(df, 'timestamp')
    return ticker

if __name__ == '__main__':
    df = calc()
    print(df['macdh'])


    #  collection.drop()
    #  BtcTrade('eth').init()
    # print(list(collection.find()))
    #  app.run(host="0.0.0.0", port=8000, debug=True)
