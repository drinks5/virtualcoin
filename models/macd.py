# encoding: utf-8
import pandas as pd
import numpy as np
from datetime import datetime
from .data import collection


def makedata():
    now = datetime.now()
    today = datetime(now.year, now.month, now.day).timestamp()
    df = pd.DataFrame.from_records(
        collection.find({
            'timestamp': {
                '$gt': today
            }
        }).sort('timestamp', 1))
    df = df.groupby(
        pd.cut(df["timestamp"],
               np.arange(df['timestamp'].min(), df['timestamp'].max(), 1 *
                         60))).sum()
    df['date'] = df['timestamp'].map(datetime.fromtimestamp)
    df = df.set_index(['date'])
    return df


def macd(func):
    def inner(*args, **kwargs):
        df = func(*args, **kwargs)
        df['ema26'] = pd.ewma(df['close'], span=26)
        df['ema12'] = pd.ewma(df['close'], span=12)
        df['macd'] = df['ema12'] - df['ema26']
        return df

    return inner


def inotify(func):
    def inner(*args, **kwargs):
        df = func(*args, **kwargs)
        last = df.tail(2).filter(['close', 'macd'])
        pre, last = last.iloc[0], last.iloc[1]
        if last['macd'] * pre['macd'] < 0:
            if last['macd'] < 0:
                info = '卖出'
            else:
                info = '买入'
            print('macd 突破0轴 ' + info)
            print(last.to_string())
        return df
    return inner


def draw(func):
    def inner(*args, **kwargs):
        df = func(*args, **kwargs)
        df.plot(y=['close'], title='Close')
        df.plot(y=['macd', 'Signal Line'], title='MACD & Signal Line')
        df.plot(
            y=['Centerline Crossover', 'Buy Sell'],
            title='Signal Line & Centerline Crossovers',
            ylim=(-3, 3))
        df['Centerline Crossover'] = np.where(df['macd'] > 0, 1, 0)
        df['Signal Line'] = pd.ewma(df['macd'], span=9)
        df['Signal Line Crossover'] = np.where(df['macd'] > df['Signal Line'],
                                               1, 0)
        df['Signal Line Crossover'] = np.where(df['macd'] < df['Signal Line'],
                                               -1, df['Signal Line Crossover'])
        df['Centerline Crossover'] = np.where(df['macd'] > 0, 1, 0)
        df['Centerline Crossover'] = np.where(df['macd'] < 0, -1,
                                              df['Centerline Crossover'])
        df['Buy Sell'] = (2 * (np.sign(df['Signal Line Crossover'] -
                                       df['Signal Line Crossover'].shift(1))))
        return df


if __name__ == '__main__':
    df = inotify(macd)(makedata)()
    print(df['macd'])
