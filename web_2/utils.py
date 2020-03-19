import time
import random


def log(*args, **kwargs):
    # time.time() return unix time
    # how to transform the Unix Time to a form that we can understand?
    # time_format = '%Y/%m/%d %H:%M:%S'
    time_format = '%m/%d %H:%S'
    value = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, value)
    print(formatted, *args, **kwargs)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(formatted, *args, file=f, **kwargs)


def random_string():
    """
    give some strs.
    :return:
    """
    seed = 'lksjdfasnchvieronnmbvmcx342356576834'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s