import pymongo
import json
import requests
from datetime import datetime

from sanic import Sanic

app = Sanic(__name__)

# pymongo.MongoClient("localhost", 27017)

# db = client.test

formatmap = {"hourly": "%H:%M",
             'daily': '%Y-%m-%d %H:%M'}

@app.websocket('/feed')
async def feed(request, ws):
    url = 'https://plugin.sosobtc.com/widgetembed/data/period?symbol=btctradeethcny&step=900'
    format = 'daily'
    while True:
        response = requests.get(url).json()[-1 * 60 * 5:]
        dates = (int(x[0]) for x in response)
        dates = [datetime.fromtimestamp(x).strftime(formatmap[format]) for x in dates]

        dataset = [x[1:] for x in response]
        await ws.send(json.dumps(dict(dates=dates, dataset=dataset)))
        data = await ws.recv()
        print('Received: ' + data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
