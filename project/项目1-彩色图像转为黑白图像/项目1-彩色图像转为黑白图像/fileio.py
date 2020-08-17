"""
先看这个链接
http://www.runoob.com/python/python-files-io.html


当我们使用 import xx 语句的时候，如下所示
import gua
会执行 gua.py 文件里面的代码

所以 gua.py 这种会被 import 的文件里面只应该有 定义，不应该有 调用
而我们之前用的方式是在文件最下方调用 __main()

用如下的方式规避这个问题
python 有一个内置变量叫 __name__
当文件被 import 的时候执行的时候 __name__ 的值是模块名（就是 import 的名字）
当文件被单独运行的时候 __name__ 的值是 '__main__'

所以我们要求用下面的代码
if __name__ == '__main__':
    main()
来替换之前的直接调用
main()

这样单独运行文件的时候就会执行 main()
而 import 文件的时候则不会执行
"""


log = print


def read_file():
    # path 是要打开的文件的路径，由于在当前目录下所以只需要写文件名就可以了
    path = 'gua.txt'
    # 下面的 open 函数第二个参数 'r' 是默认值，所以也可以不用传
    # with open(path) as f:
    #
    # 注意这个 with 语法，你在其他地方可能看不到这个写法
    # 但是现在 with 是打开文件的标准写法，必须这样写
    # f 就是被打开的文件
    # f.read() 就是返回文件的所有内容
    with open(path, 'r') as f:
        s = f.read()
        return s


def write_file():
    path = 'gua.txt'
    # 'w' 表示要写入文件，注意这个写入是覆盖式写入，原来的文件的所有内容都会被替换
    # 如果这个文件不存在就创建它
    with open(path, 'w') as f:
        s = 'hello gua'
        # write 用于写入字符串内容到文件
        f.write(s)


def main():
    # 在当前目录写入一个 gua.txt 文件
    write_file()
    # 读取刚才写入的内容并 log 出来
    s = read_file()
    log('read file', s)


# 这里使用 main 而非 __main 的原因是别人都用 main
# 随大流比较好，跟别人不一样容易遭受非议
if __name__ == '__main__':
    main()
