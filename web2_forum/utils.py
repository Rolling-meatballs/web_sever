import time


def log(*args, **kwargs):
    """
    :param args:
    :param kwargs:
    """
    # time.time() return unix time
    # transform unix time to normal form human kind
    format_ = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format_, value)
    with open('bug.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, **kwargs)
        print(dt, *args, file=f, **kwargs)
