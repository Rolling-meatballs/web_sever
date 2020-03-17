import time
import random


def log(*args, **kwargs):
    # time.time() return unix time
    # how to transform the Unix Time to a form that we can understand?
    # time_format = '%Y/%m/%d %H:%M:%S'
    time_format = '%m/%d %H:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)


def random_string():
    """
    give some strs.
    :return:
    """
    seed = 'lksjdfasnchvieronnmbvmcx'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s