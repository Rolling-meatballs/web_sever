'''
项目 10


本次需要给之前做的词典软件加上单词读音功能

界面上增加一个读音按钮，按了后会播放单词的语音
播放单词语音的具体做法见如下描述

播放单词语音需要两步
1，获取到语音文件
2，用 kivy 播放这个语音文件

在项目 4 的说明中有如下部分内容
截取如下（删除了多余的部分）
其中 symbols 的 ph_am_mp3 里存的是单词的美式发音 mp3 文件
{
    "word_name": "name",
    "symbols": [{
        "ph_en_mp3": "http://res.iciba.com/resource/amp3/oxford/0/1b/c3/1bc38ba928f40072e7c62d427a05c03e.mp3",
        "ph_am_mp3": "http://res.iciba.com/resource/amp3/1/0/b0/68/b068931cc450442b63f5b3d276ea4297.mp3",
        "ph_tts_mp3": "http://res-tts.iciba.com/b/0/6/b068931cc450442b63f5b3d276ea4297.mp3",
    }]
}

我们可以下载并保存这个 mp3 文件然后播放
比如例子这个文件可以保存为 name.mp3 （因为有 word_name）

下载文件并保存的代码如下
为了把单词语音保存为 单词名.mp3 的形式你需要修改这个函数
def download(url):
    path = '文件名.mp3'
    s = urllib.request.urlopen(url).read()
    # 'w' 表示写入  'b' 表示二进制模式
    with open(path, 'wb') as f:
        f.write(s)
'''

# 下面的例子下载了一个 mp3 文件并保存为 文件名.mp3 
import urllib.request


def download(url):
    path = '文件名.mp3'
    s = urllib.request.urlopen(url).read()
    # 'w' 表示写入  'b' 表示二进制模式
    with open(path, 'wb') as f:
        f.write(s)


def main():
    # 注意，这里一定要有查单词的那个 key，否则下载是不成功的
    key = ''
    ph_am_mp3 = "http://res-tts.iciba.com/b/0/6/b068931cc450442b63f5b3d276ea4297.mp3"
    url = '{}?key={}'.format(ph_am_mp3, key)
    download(url)


if __name__ == '__main__':
    main()
