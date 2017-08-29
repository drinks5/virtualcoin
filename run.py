# encoding: utf-8
import sys
from models.macd import macd, makedata, inotify
from models.data import BtcTrade


if __name__ == '__main__':
    if 'data' in sys.argv:
        BtcTrade(hooks=macd(makedata)).forever()
    df = inotify(macd(makedata))()
    print(df['macd'])
