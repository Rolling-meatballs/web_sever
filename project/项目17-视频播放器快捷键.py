"""
kivy 实现快捷键方法

1，在 Window 上绑定快捷键，它在 kivy.core.window 中

2，绑定方式为 Window.bind(on_keyboard=self.on_keyboard)

3，在 self.on_keyboard 中来判断执行的事件，这个函数原型如下，参数含义自己实验
on_keyboard(key, scancode=None, codepoint=None, modifier=None, **kwargs)

要求：
实现左右箭头快退快进 10s 的功能
实现上下箭头快进快退 60s 的功能
实现空格暂停/播放功能
"""
