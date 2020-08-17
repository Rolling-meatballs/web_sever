from PIL import Image
# 像安装 cocos2d 一样安装 PIL 库, 方法如下
# pip3 install pillow
# 这是 python 用于处理图像文件的库


"""
下面介绍一下计算机存储图像的原理

w 是图像宽
h 是图像高
一个图像由 w * h 个像素点组成
每个像素点由 rgba 4 个部分组成
r 红色
g 绿色
b 蓝色
a 透明度

现在的图像 rgba 分别是一个字节表示，一个字节的数值范围是 0 - 255
也就是一个像素点 4 字节，可以表示的颜色范围是 256 的 4 次方

但是很多图像是没有 a 的，所以就只有 3 字节表示一个像素



作业要求：
参考下面的链接和本文件的代码
https://baike.baidu.com/item/%E5%8E%BB%E8%89%B2

实现 grayscale 函数，让生成的 gua.png 是黑白的
"""


log = print


def grayscale(R, G, B, a):


    # 由于 python 用缩进表示代码结构
    # 所以发明了一个 pass 语句
    # 这个语句没有其他作用，只是一个占位符
    # 如果没有 pass 直接留空函数就会有语法错误
    Gray =(R + G + B )// 3


    # log('img', image.width)
    # pass
    return Gray


def main():
    # 打开图像文件
    img = Image.open("gua_sample.png")
    # 注意由于不是每个图像都有 a 所以这里强制转换成 RGBA 格式
    img = img.convert('RGBA')

    # 读取座标 (1, 2) 处的像素点的像素值
    width, height = img.size
    for i in range(width):
        for a in range(height):
            position = (i, a)
            r, g, b, a = img.getpixel(position)
            # log('get pixel', r, g, b, a)

    # 把座标 position 的像素值改写为 白色（全发光就是白色，0 0 0 0 是黑色）
    #         img.putpixel(position, (255, 255, 255, 255))
    #         if r == g == b:
    #             break

            r = grayscale(r, g, b, a)
            img.putpixel(position, (r, r, r, a))
            log('get pixel', r, g, b, a)

    # 保存图像文件
    img.save('gua.png')
    img.show()


if __name__ == '__main__':
    main()
