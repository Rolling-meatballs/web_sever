# 先介绍一个新函数, 原型如下
# mode 是字符串, 我们使用 'RGBA' 表示生成一个每个像素由 rgba 四字节组成的图片
# size 是一个 (w, h) 表示宽高的 tuple
#
# Image.new(mode, size)


# 例子如下

from PIL import Image

# 生成一个宽高都是 100 的 rgba 模式的图片
# img = Image.new('RGBA', (100, 100))

log = print


# 实现以下几个函数

def crop(image, frame):
    """
    image 是一个 Image 对象
    frame 是一个 tuple 如下 (x, y, w, h)
        用于表示一个矩形的左上角座标 x y 和 宽高 w h

    不修改原图像
    返回一个 Image 对象, 它是用 frame 把 image 裁剪出来的新图像
    """
    pass


def flip(image):
    """
    image 是一个 Image 对象

    不修改原图像
    返回一个 Image 对象, 它是 image 上下镜像的图像
    """
    pass


def flop(image):
    """
    image 是一个 Image 对象

    不修改原图像
    返回一个 Image 对象, 它是 image 左右镜像的图像
    """
    pass


def main():
    """
    压缩包内有图片 a.jpg
    图片是面朝左的 doge 加下方的四个字
    要求生成一张图片 b.jpg, 狗头朝右但下方文字不变
    """
    img = Image.open('b.jpg')
    img = img.convert('RGBA')
    i = crop(img, (0, 0, 50, 20))
    # i.save('crop.png')
    # i = flip(img)
    # i.save('flip.png')
    # i = flop(img)
    i.show()
    i.save('b.jpg')
    pass


if __name__ == '__main__':
    main()
