from kivy.app import App
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
# 用于播放声音
from kivy.core.audio import SoundLoader

'''
本次作业要给上次的 播放器 软件加入暂停和进度条显示功能

1，暂停
参考上次的作业
kivy 的声音并没有提供 pause() 方法，但是我们翻看文档有如下描述
seek 方法用于设置播放的位置，但是描述中说必须先 play 再 seek
seek(position)
Go to the <position> (in seconds).
Note：Most sound providers cannot seek when the audio is stopped. Play then seek.

这样我们的思路就很简单了，暂停的时候记录当前播放时间，播放的时候 seek 到那个时间
这样就实现了播放暂停功能

仿造传统播放器的做法，把暂停/播放功能放在一个按钮上，用一个变量来记录状态，点击按钮的时候改变文字显示（播放/暂停）


2，进度条显示功能（不能拖拽，只提供进度显示）
由于 kivy 并未提供好用的进度条控件，所以我们得自己实现一个
听起来很困难实际上很简单
最简单的进度条其实就是两个不同颜色的矩形叠加
然后定时更新上层矩形的宽度
如果有任何问题，请在群内讨论思路
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
