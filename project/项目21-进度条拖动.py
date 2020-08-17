from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
# 引入 video
from kivy.uix.video import Video
from kivy.uix.button import Button

from kivy.core.window import Window

log = print


"""
本次项目需要给播放器点击和拖动进度条的功能
（无论音乐播放器还是视频播放器原理都是一样的）


具体方法如下

1, 用按钮作为总进度条，给它绑定点击事件和松开事件

2, 给 Window 绑定鼠标移动事件

3, 按钮点击后获取点击坐标并保存，设置一个点击状态

4, 鼠标移动的时候检查当前是否是点击的状态
    如果是，则计算并设置进度条

5, 按钮松开后要改写点击状态，这样鼠标移动的时候就不会设置进度条了

6, 跳转到新时间播放，设置方法如下
    # new_time 是一个在 0 - 1 之间的小数
    self.video.seek(new_time)


需要注意的是，由于进度条的 x 未必是 0
所以你在计算的时候要考虑到这个问题
请查看本程序来获取示例
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
        Config.set('graphics', 'width', 200)
        Config.set('graphics', 'height', 300)

    def setup_ui(self):
        layout = FloatLayout()
        self.bar = Button(
            text='click',
            pos=(100, 200)
        )
        self.bar.bind(on_press=self.click)
        self.bar.bind(on_release=self.release)

        # 获取鼠标位置
        Window.bind(mouse_pos=self.on_mouse_move)
        # self.bar.bind(mouse_pos=self.on_mouse_move)
        #
        layout.add_widget(self.bar)
        return layout

    def on_mouse_move(self, window, position):
        """
        鼠标在界面内移动显示控件
        鼠标静止不动 3 秒消失
        """
        log('移动中', window, position)
        self.mouse_position = position

    def click(self, *args):
        print('click args', self.mouse_position)

    def release(self, *args):
        print('release args', self.mouse_position)

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
        pass


def main():
    # 生成 App 并运行
    TestApp().run()


if __name__ == '__main__':
    main()
