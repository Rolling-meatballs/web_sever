from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
# 引入 video
from kivy.uix.video import Video


log = print


"""
本次作业需要实现一个视频播放器，框架代码如下
你需要看懂这个程序，然后添加如下功能：
1，播放按钮
2，暂停按钮
3，进度条
4，音量显示
5，音量加减 2 个按钮，每次调整 5%

你需要放一个 demo.mp4 文件在相同文件夹
"""


def font_name():
    """
    苹果系统和微软系统需要不同的字体文件
    """
    from sys import platform
    if platform == 'darwin':
        return 'Arial Unicode'
    elif platform == 'win32':
        return 'SimHei'
    else:
        print('not support')


class TestApp(App):
    # build 函数是固定的, 它用于生成界面
    def build(self):
        self.config_window()
        root = self.setup_ui()
        return root

    def config_window(self):
        """
        这里设置了 3 个属性, 这是固定的写法
        分别是 禁止缩放, 宽度 400, 高度 600
        """
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'width', 400)
        Config.set('graphics', 'height', 600)

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical')
        # 请注意，由于 kivy 的官方实现 video 是有 bug 的
        # 所以官方文档也是错的，你要按照我给的这样的例子来写才行，这是我看源码扒出来的可行方法
        # 自动播放的写法
        v = Video(source='demo.mp4', state='play')
        self.video = v
        # on_loaded 函数会在视频载入成功后被调用
        v.bind(texture_size=self.on_loaded)
        # on_position_change 函数会在视频播放的时候不断调用，具体你播放一下就好了
        v.bind(position=self.on_position_change)
        layout.add_widget(v)
        return layout

    def on_position_change(self, video, value):
        print('The position in the video is', value)

    def on_loaded(self, video, value):
        print('视频已经载入')
        v = video
        # 由于视频会自动播放，所以在载入函数这里可以用 v.state = 'pause' 暂停视频
        # v.state = 'pause'
        # 视频暂停后可以用 v.state = 'play' 播放视频
        log('视频时长，单位 秒', v.duration)
        log('视频尺寸，单位 像素', v.texture_size)


def main():
    # 生成 App 并运行
    TestApp().run()


if __name__ == '__main__':
    main()
