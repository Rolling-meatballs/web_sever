from kivy.app import App
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

# 用于播放声音
from kivy.core.audio import SoundLoader

'''
本次作业要做一个 播放器 软件, 以后的项目中会把这个软件功能完善, 这只是初步的阶段

为了实现播放声音, 本次引入了一个新的类 SoundLoader
具体用法很简单, 下面第一行加载声音返回一个类, 第二行调用 play() 方法播放
audio = SoundLoader.load('mipha.mp3')
audio.play()        # 播放声音


audio.stop()        # 停止播放
audio.get_pos()     # 当前播放到的时间, 单位是秒, 只有在播放的时候才能获取, 否则是 0
audio.length        # 声音的长度, 单位是秒
audio.volume = 1    # 设置/读取音量, 值范围是 0 到 1, 1 是最大音量

详细介绍可以参考官方文档(不建议, 本作业用不着)
https://kivy.org/docs/api-kivy.core.audio.html


界面要求 3 个控件
1, 显示播放进度的 label, 格式如下(当前时间 分:秒 / 总时间 分:秒)
    00:00/04:12
2, 播放按钮
    开始更新播放进度, 一秒更新一次
3, 停止按钮
    停止更新播放进度并且播放进度清零, 声音停止
'''

log = print

def font_name():
    """
    苹果系统和微软系统需要不同的字体文件
    """
    from sys import platform
    if platform == "darwin":
        return 'Arial Unicode'
    elif platform == "win32":
        return 'SimHei'
    else:
        print('not support')


class TestApp(App):
    def build(self):
        self.config_window()
        root = self.setup_ui()
        return root

    def config_window(self):
        """
        这里设置了 3 个属性, 这是固定的写法
        分别是 禁止缩放, 宽度 400, 高度 600
        """
        g = 'graphics'
        Config.set(g, 'resizable', False)
        Config.set(g, 'width', 400)
        Config.set(g, 'height', 600)

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical')
        # 注意，你需要在当前目录放一个音乐文件并替换 a.mp3 这个名字为你的音乐文件
        audio = SoundLoader.load('a.mp3')
        audio.play()
        return layout


def main():
    TestApp().run()


if __name__ == '__main__':
    main()
