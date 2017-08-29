# encoding: utf-8
import logging

import functools


def log(text):
    print(text)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print(args)
            print('%s %s():' % (text, func.__name__))
            result = func(*args, **kw)
            print('result %s' % result)
            return 's' + result

        return wrapper

    return decorator


@log('log')
def f(arg):
    print('f')
    return 'b'


f

print('---')
f('a')

if __name__ == '__main__':
    print('test')
