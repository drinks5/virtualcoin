# encoding: utf-8
import sys
import time
from models.macd import macd, makedata, inotify
from models.data import BtcTrade


if __name__ == '__main__':
    if 'data' in sys.argv:
        BtcTrade(hooks=macd(makedata)).forever()
    while True:
        df = inotify(macd(makedata))()
        print(df['macd'])
        time.sleep(30)
