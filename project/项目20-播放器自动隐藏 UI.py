"""
本次要给视频播放器加入自动隐藏 UI 的功能
具体需求是鼠标静止不动 3 秒后，隐藏播放器的控制 UI

主要有 2 个技术点
1, 在 kivy 中如何监听鼠标移动事件
2, 在 kivy 中如何隐藏一个控件

文档里面的监听鼠标移动事件的方法如下，但是这个方案是错误的
请参考本程序的方法监听鼠标移动事件
Window.bind(on_mouse_move=self.on_mouse_move)


隐藏控件最好的方式是直接设置控件的坐标，让它在窗口尺寸之外即可

那具体的做法就是设置用一个变量记录鼠标移动的时间
另外再用一个定时器每隔 0.5 秒（或者更小的事件间隔）去检测是否应该隐藏 UI
这当然不是完美的算法，但是这是可行的算法
这 2 个都是在最初的项目中有例子的，不懂的话群内讨论
"""
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window


log = print


class TestApp(App):
    def build(self):
        root = self.setup_ui()
        return root

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical')
        self.button1 = Button(text='hello', font_size=14)
        layout.add_widget(self.button1)
        # 引入 window 库
        Window.bind(mouse_pos=self.on_mouse_move)
        return layout

    def on_mouse_move(self, window, position):
        """
        鼠标在界面内移动显示控件
        鼠标静止不动 3 秒消失
        """
        log('移动中', window, position)


def main():
    # 生成 App 并运行
    TestApp().run()


if __name__ == '__main__':
    main()
