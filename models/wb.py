from datetime import datetime
import json

from sanic import Sanic
from .data import collection

app = Sanic(__name__)


formatmap = {"hourly": "%H:%M", 'daily': '%Y-%m-%d %H:%M'}
keys = ['date', 'amount', 'close', 'high', 'low', 'open', 'volume']


@app.websocket('/feed')
async def feed(request, ws):
    format = 'daily'
    query = {}
    querystring = ''
    while True:
        querystring.isdigit() and query.update(
            timestamp={"$gt": int(querystring)})
        response = collection.find(query)
        dates = (x['timestamp'] for x in response)
        dates = [
            datetime.fromtimestamp(x).strftime(formatmap[format])
            for x in dates
        ]
        dataset = [x['data'] for x in response]
        await ws.send(json.dumps(dict(dates=dates, dataset=dataset)))
        querystring = await ws.recv()
