"""
1, 把本文件改成 main.py 文件名


2, 今后需要编写图形界面程序, 我们使用 kivy 这个开发框架来做这件事, 先安装 kivy

Windows 安装方法:
    0, 打开 cmd

    1, 输入 python --version 检查并确保安装的是否是 Python 3.6.5

    2, 在命令行输入以下命令进行安装，需要一定的时间，耐心等待，如果有错误到群里提问讨论
    python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple docutils==0.14 pygments==2.2.0 pypiwin32==223 kivy.deps.sdl2==0.1.18 kivy.deps.glew==0.1.10 kivy.deps.gstreamer==0.1.12 kivy==1.10.0


Mac 安装方法(请严格按照指令执行, 不要自创):
    0, 下载群文件中的 Kivy-1.10.0-osx-10.12.5-python3.5.dmg 文件

    1, 确保你的系统是 10.12 以上

    2, 双击 dmg 文件打开, 把 Kivy.app 拖入 /Applications 目录

    3, 完成步骤 2 后
        1) 右键(必须右键) MakeSymlinks 文件
        2) 点击打开
        3) 在弹出的对话框中点再点击打开
        4) 弹出的终端窗口显示 [Process completed] 后可以关闭

    4, 进入 /Applications 目录找到 Kivy.app 文件
        1) 右键(必须右键)
        2) 点击打开
        3) 在弹出的对话框中点再点击打开


3, 运行程序
可以使用 Pycharm 编辑代码

Windows 运行代码方法:
在 pycharm 中运行

Mac 运行代码方法
把代码放在桌面上, 改名为 main.py
运行代码需要在 终端 中进行
打开终端, 输入下面的命令运行程序(可以复制粘贴)
kivy ~/Desktop/main.py



4, 参考下面的代码, 结合项目 4, 实现一个图形化查词软件
"""
from kivy.app import App
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


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
        Config.set('graphics', 'width', 400)
        Config.set('graphics', 'height', 600)

    def setup_ui(self):
        """
        程序窗口必须有一个 layout(布局), 所有的按钮/文本框之类的东西都必须添加在布局中
        我们把 按钮 文本框 这类的东西叫做 控件
        我们这里用了 boxlayout, 先不管, 用起来
            orientation='vertical' 表示这个 layout 里面的东西是竖直排列的
            竖直排列的情况下, 一个控件默认是横向填满, 平分高度
            这个例子中我们添加了 2 个文本框, 所以他们每个占据一半的高度
        """
        layout = BoxLayout(orientation='vertical')
        # textinput 是文本输入框, multiline=False 表示这是一个单行文本框
        input = TextInput(multiline=False)
        # 给 input 绑定一个事件 on_text_validate
        # 这个事件是在按回车的时候触发的, 也就是说你按回车的时候 self.check 函数会被调用
        input.bind(on_text_validate=self.check)
        layout.add_widget(input)
        # 
        result = TextInput()
        # kivy 默认不支持中文字符显示, 必须手动指定包含中文的字体文件才可以显示中文
        # 因为 mac 和 win 的字体文件不同, 所以我们用一个函数来判断具体使用哪个字体文件
        result.font_name = font_name()
        layout.add_widget(result)
        # 把 result 这个输入框用类的属性存起来之后要使用
        # 类属性在类的任何函数中都可以创建, 并不一定要在 __init__ 中创建
        self.result = result
        # 
        return layout

    def check(self, input):
        """
        input 就是触发回车的输入框控件
        """
        # input.text 可以获取这个输入框中输入的文本
        print('check, ', input.text)
        s = input.text + '\n' + 'done'
        # 我们在这里可以设置 result 输入框的文本
        self.result.text = s


def main():
    # 生成 App 并运行
    TestApp().run()


if __name__ == '__main__':
    main()
