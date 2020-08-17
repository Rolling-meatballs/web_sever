from kivy.app import App
from kivy.config import Config

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

from kivy.metrics import dp


log = print


"""
本项目要给之前做的 播放器 软件添加播放列表支持

给播放器添加播放列表的步骤如下
1，让整个界面宽度翻倍，并平分为 2 个部分。
    layout 里面可以嵌套其他的 layout
    如果这个功能不会做，请在群内讨论
2，左边是老的播放界面，右边是播放列表


因为播放列表可能很长，所以要实现播放列表，需要一个可以滚动内容的方案
请参考下面的代码的工作原理来实现播放列表


功能如下：
1，播放列表中的文件是写死的几个文件，你自己来写好
2，点击播放列表中相应的名字的时候，要开始播放相应的 mp3 文件
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
        self.setup_bg(layout)
        # 添加按钮
        self.setup_button(layout)
        # 添加列表组件
        self.setup_listview(layout)
        return layout

    def setup_bg(self, layout):
        bg = Image(
            pos=(0, 0),
            size=(dp(400), dp(600)),
            size_hint=(None, None),
        )
        layout.add_widget(bg)

    def setup_button(self, layout):
        button = Button(
            background_down='play.png',
            background_normal='play.png',
            border=(0, 0, 0, 0),
            size=(dp(64), dp(64)),
            size_hint=(None, None),
            pos=(dp(100), dp(100)),
        )
        button.bind(on_press=self.press)
        layout.add_widget(button)

    def setup_listview(self, layout):
        """
        这个函数演示了如何制作一个列表
        """
        # 这个 gridlayout 不要改动
        gl = GridLayout(
            cols=1,
            spacing=dp(2),
            size_hint_y=None,
        )
        gl.bind(minimum_height=gl.setter('height'))
        # 往 gl 中添加 30 个 Button, 这里可以换成你想要显示的列表，比如 label
        for i in range(30):
            btn = Button(text=str(i), size_hint_y=None, height=40)
            gl.add_widget(btn)
        # 把 gl 装入 scroll 中，尺寸由 scroll 规定，这样就可以滚动了
        scroll = ScrollView(
            pos=(dp(100), dp(100)),
            size=(dp(200), dp(300)),
            size_hint=(None, None),
            bar_width=dp(10),
        )
        scroll.add_widget(gl)
        layout.add_widget(scroll)

    def press(self, button):
        button.background_normal = 'pause.png'
        print('press', button)


def main():
    # 生成 App 并运行
    TestApp().run()


if __name__ == '__main__':
    main()
