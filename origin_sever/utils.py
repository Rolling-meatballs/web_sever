import time


def log(*args, **kwargs):
    """
    用这个log 代替 print
    time.time() 返回 unix time
    把 unix time 转换为普通人能看懂的格式
    """
    time_format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print('web', *args, **kwargs)
