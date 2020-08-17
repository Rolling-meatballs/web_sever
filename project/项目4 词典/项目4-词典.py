# 1. 介绍 json
# 下面是一个存储了单词 name 的释义的 json 格式字符串
# 你可以简单地把它看为一个字典，并且我们可以用标准库 json 轻松把这个字符串转为 python dict
# 它的结构和字典一样

# 2. 介绍数据含义
# 这个 释义 是从爱词霸的服务器上获取的，我们先不管获取的方法，先关心里面存储的数据的含义
# word_name 是被查询的单词
# is_CRI 不需要关心，可以忽略
# exchange 是一个字典，包含了单词的所有形式（复数、过去时等）
# symbols 是一个数组，目前里面只包含了一个字典
#   其中有 3 个 mp3 文件的链接，分别是英音、美音、语音合成音
#   parts 是一个数组，里面包含了单词 name 所有的含义
"""
{
    "word_name": "name",
    "is_CRI": "1",
    "exchange": {
        "word_pl": [
            "names"
        ],
        "word_third": [
            "names"
        ],
        "word_past": [
            "named"
        ],
        "word_done": [
            "named"
        ],
        "word_ing": [
            "naming"
        ],
        "word_er": "",
        "word_est": ""
    },
    "symbols": [{
        "ph_en_mp3": "http://res.iciba.com/resource/amp3/oxford/0/1b/c3/1bc38ba928f40072e7c62d427a05c03e.mp3",
        "ph_am_mp3": "http://res.iciba.com/resource/amp3/1/0/b0/68/b068931cc450442b63f5b3d276ea4297.mp3",
        "ph_tts_mp3": "http://res-tts.iciba.com/b/0/6/b068931cc450442b63f5b3d276ea4297.mp3",
        "parts": [{
                "part": "n.",
                "means": [
                    "名字",
                    "名声",
                    "有…名称的",
                    "著名的人物"
                ]
            },
            {
                "part": "vt.",
                "means": [
                    "确定",
                    "决定",
                    "给…取名",
                    "说出…的名字"
                ]
            },
            {
                "part": "adj.",
                "means": [
                    "著名的",
                    "据以取名"
                ]
            }
        ]
    }]
}
"""

# 3. 使用 json 标准库解析 json 格式字符串为 python 的 dict
"""
import json


s = '''
{
    "name": "gua",
    "height": [
        169,
        1.69
    ]
}
'''

d = json.loads(s)

print('result', d['name'], d['height'][1])
# 结果如下
# result gua 1.69
"""


# 4. 获取单词释义的 json 格式字符串
"""
1) 打开爱词霸网站，链接如下
http://open.iciba.com/?c=api

2）选择词霸查词
    输入网址名称、网址和你的邮箱地址（网址名称和网址可随意填写）
    提交后邮箱会收到一个邮件包含身份 key

3）用如下的代码获取到单词释义的 json 格式字符串
# 输入你的身份 key
key = ''
word = 'name'
url = 'http://dict-co.iciba.com/api/dictionary.php?type=json&key={}&w={}'.format(key, word)

# openurl 是课 4 作业 14 的 openurl 函数
# 用来获取网络词典返回的结果
s = openurl(url)
"""

"""
作业要求：
本作业需要按照上面的顺序描述实现一个词典软件
实现 translate 函数，输出所有的单词含义
例如对于 name 这个单词，输出如下
n.
名字
名声
有…名称的
著名的人物

vt.
确定
决定
给…取名
说出…的名字

adj.
著名的
据以取名
"""

import json
import urllib.request

log = print

def openurl(word):
    key = 'E442BF444FCC75B0CBD92D3D941B4FE0'
    url = 'http://dict-co.iciba.com/api/dictionary.php?type=json&key={}&w={}'.format(key, word)
    s = urllib.request.urlopen(url).read()
    content = s.decode('utf-8')
    return content


def translate(word):
    """
    word 是一个不包含空格的单词
    """
    s = openurl(word)
    d = json.loads(s)

    a = d['symbols'][0]
    # log(a)
    log(d['word_name'], ':')

    two = []
    for i in range(3):
        b = a.get('parts')[i]
        # log(b.get('part'))
        c = b.get('means')
        aone = []
        aone.append(b.get('part'))
        for I in range(len(c)):
            aone.append(c[I])
            # log(aone)

            # log(c[I])
        # log('\n')
        two.append(aone)
    log(two)


    # pass


def main():
    word = 'name'
    translate(word)


if __name__ == '__main__':
    main()
