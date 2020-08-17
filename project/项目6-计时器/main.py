"""
本项目需要实现一个计时器程序
界面原型在压缩包内, 文件名是 prototype.png
你的程序界面和原型不需要一模一样, 大致是这样就好了

注意显示的格式是 00:00:00 分别表示 分:秒:毫秒
毫秒到秒的进位是 1000, 注意换算


为了实现这个程序我们需要以下的功能
1, 获取当下的时间
2, 定时更新时间显示(比如每秒更新 10 次)
3, 按钮和按钮点击事件(和项目 4 的回车事件一个性质)


1, 把本文件改成 main.py

2, 在 python 中获取当前的时间的方法如下
import time

time.time()
# 返回一个小数, 代表的是当前的时间, 单位为 秒
# 那么下次再调用这个函数得到的时间减去这个时间就是时间差
# 1527227483.985863

3, kivy 中的定时器例子已经在下面的代码中了

4, 参考下面的代码, 实现一个计时器
    开始按钮开始计时并更新时间显示
    暂停按钮停止计时并定格时间显示
    重置按钮停止计时并重置时间为 00:00:00


有思路上的问题, 请在群内讨论
"""
from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import time

# 在 retina 屏幕上(比如 macbook pro 系列), 需要使用这个 dp 函数来转换像素坐标
# 具体用法见下方代码中的注释说明
from kivy.metrics import dp


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


# 程序一定是一个继承自 App 的 xxApp 类作为起点
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
        # 注意这里窗口的宽高是不需要用 dp 的, kivy 就这么设计的
        Config.set('graphics', 'width', 400)
        Config.set('graphics', 'height', 200)

    def setup_ui(self):
        """
        程序窗口必须有一个 layout(布局), 所有的按钮/文本框之类的东西都必须添加在布局中
        我们把 按钮 文本框 这类的东西叫做 控件
        项目 5 使用了 boxlayout, 这里我们使用 floatlayout 它可以自定义控件的尺寸和座标
        """
        layout = FloatLayout(size=(400, 600))
        # 参数太多, 所以这样方便一点
        input_config = {
            'multiline' : False,        # 单行
            'pos' : (dp(50), dp(150)),   # 坐标, 原点在窗口左下角, 用 dp(像素) 可以让程序在 retina 屏幕上使用期望的坐标
            'size' : (dp(300), dp(40)),# 尺寸 宽 高
            'size_hint' : (None, None), # 设置尺寸后必须设置 size_hint 为 (None, None) 否则尺寸设置无效
        }
        input = TextInput(**input_config)
        # 上面的写法等同于下面的写法, 这是 python 的关键字参数(**kwargs)功能
        # input = TextInput(size=(dp(400), dp(50)), size_hint=(None, None), multiline=False)
        # 给 input 绑定一个事件 on_text_validate
        # 这个事件是在按回车的时候触发的, 也就是说你按回车的时候 self.check 会被调用
        input.bind(on_text_validate=self.check)
        layout.add_widget(input)
        # 
        # 注意, 用 dict 函数也可以生成字典, 结果和上方的 input_config 是一样的
        # 这样的写法有时候更方便(比如不用给 key 加引号)
        # 注意, 这里的像素值没有使用 dp, 在普通屏幕上没有差异, 在 retina 屏幕上自行观察
        button_config_start = dict(
            text='开始',
            font_size=20,
            pos=(20, 25),
            size=(110, 50),
            size_hint=(None, None),
            font_name=font_name(),  # 字体名字也可以在初始化的时候配置
        )

        button_config_stop = dict(
            text='暂停',
            font_size=20,
            pos=(145, 25),
            size=(110, 50),
            size_hint=(None, None),
            font_name=font_name(),  # 字体名字也可以在初始化的时候配置
        )

        button_config_reset = dict(
            text='重置',
            font_size=20,
            pos=(270, 25),
            size=(110, 50),
            size_hint=(None, None),
            font_name=font_name(),  # 字体名字也可以在初始化的时候配置
        )

        button_start = Button(**button_config_start)
        button_start.bind(on_press=self.button_press)
        print('start:', button_start )

        button_stop = Button(**button_config_stop)
        button_stop.bind(on_press=self.button_press)

        button_reset = Button(**button_config_reset)
        button_reset.bind(on_press=self.button_press)

        layout.add_widget(button_start)
        layout.add_widget(button_stop)
        layout.add_widget(button_reset)
        # 把 result 这个输入框用类的属性存起来之后要使用
        # 类属性在类的任何函数中都可以创建, 并不一定要在 __init__ 中创建
        # self.button_start = button_start
        # self.button_stop = button_stop
        # self.button_reset = button_reset
        # 
        label_config = dict(
            text='00:00:00',
            font_size=50,
            halign='center',    # 横向居中显示
        )
        label = Label(**label_config)
        layout.add_widget(label)
        # 定时器用法
        # 第一个参数是定时会被调用的函数
        # 第二个参数是调用的间隔时间, 单位是秒, 0.1 表示每秒调用 10 次, 这里是 1 表示每秒调用一次
        second = 0
        second = Clock.schedule_interval(self.timer, 1)

        # str_second = str(second)
        # r_time = '00:00:' + str_second
        # print("r_time", r_time)

        # label_config = dict(
        #     text=r_time,
        #     font_size=10,
        #     halign='center',  # 横向居中显示
        # )
        # label = Label(**label_config)
        # layout.add_widget(label)

        return layout

    # dt 意思是 delta-time, 间隔时间
    def timer(self, dt, recent_second):
        # 需要注意的是 dt 并不是完全精准的定时器间隔, 但这无所谓
        # 而且我们使用的是 time.time() 获取时间, 所以 dt 参数在本程序中是无用的
        print('定时器', dt)

        # recent_sechnd += 1

        print('recent time', recent_second)

        # if recent_second > 59:
        #     recent_mintues += 1
        #     if recent_mintues > 59:
        #         recent_hour += 1
        # print('recent_hour', recent_hour)

        return recent_second

    def button_press(self, button):
        # if :
        pass

        print('点击按钮', button)

    def check(self, input):
        """
        类的方法都有 self 这个参数作为第一个参数
        input 就是触发回车的输入框
        """
        # input.text 可以获取这个输入框中输入的文本
        print('check, ', input.text)
        s = input.text + '\n' + 'done'
        # 我们在这里可以设置 result 输入框的文本
        # self.result.text = s


def main():
    # 生成 App 并运行
    TestApp().run()


if __name__ == '__main__':
    main()
