from kivy.app import App
from kivy.config import Config

from kivy.uix.floatlayout import FloatLayout

from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

from kivy.metrics import dp


log = print

"""
本次作业需要实现一个功能相对完整，界面优美专业的播放器
本次的播放器不支持播放列表，只支持单曲播放

播放器界面设计参考下面的链接，选一个你能实现的
http://freefrontend.com/css-music-players/

如果选择困难，就用下面这个
https://dribbble.com/shots/998479-Music



本次需要的额外知识是
1，背景图
2，按钮切换显示

这里给出了一套播放器 UI 图标，请下载 png 格式的，这样它是透明的
https://www.flaticon.com/packs/music
"""


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
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'width', 400)
        Config.set('graphics', 'height', 600)

    def setup_ui(self):
        # 这样可以设置窗口的标题
        self.title = '播放器'
        # 
        layout = FloatLayout()
        # 添加背景图
        # self.setup_bg(layout)
        # 添加按钮
        self.setup_button(layout)
        return layout

    def setup_bg(self, layout):
        # Image 用于显示一张图片，背景色默认是白色
        bg = Image(
            pos=(0, 0),
            size=(dp(400), dp(600)),
            size_hint=(None, None),
            # source='bg.png',  # source 指定了图片
        )
        layout.add_widget(bg)

    def setup_button(self, layout):
        button = Button(
            # background_down='play.png',   # 按钮按下状态的背景图
            # background_normal='play.png', # 按钮普通状态的背景图
            border=(0, 0, 0, 0),            # 设置背景图必须设置 border 为 0 0 0 0
            size=(dp(64), dp(64)),
            size_hint=(None, None),
            pos=(dp(100), dp(100)),
        )
        button.bind(on_press=self.press)
        layout.add_widget(button)

    def press(self, button):
        # 这里可以修改按钮的背景图
        # button.background_normal = 'pause.png' # 按钮按下状态的背景图
        # button.background_normal = 'play.png', # 按钮普通状态的背景图
        print('press', button)


def main():
    # 生成 App 并运行
    TestApp().run()


if __name__ == '__main__':
    main()
