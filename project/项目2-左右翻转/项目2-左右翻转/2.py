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
    width, height = image.size
    x, y, w, h = frame
    # log(width, height)
    Imagenew = Image.new('RGBA',(w, h), 'black')
    Imagenew.save(r'C:\Users\yangf\Documents\Tencent Files\513655976\FileRecv\项目2-左右翻转\项目2-左右翻转\new.png')
    log('aaa')
    for i in range(w):
        for I in range(h):
            position = (i, I)
            r, g, b, a = image.getpixel(position)
            log('get pixel', r, g, b, a)
            Imagenew.putpixel(position, (r, g, b, a))
            log('get pixel', r, g, b, a)
            log('aaa')

    return Imagenew

    # pass


def flip(image):
    """
    image 是一个 Image 对象

    不修改原图像
    返回一个 Image 对象, 它是 image 上下镜像的图像
    """
    width, height = image.size
    for i in range(width):
        for a in range(height):

            position = (i, a)
            Position = (i, height - a - 1)
            # log(a)
            # log(i)
            if a < height - a:
                r, g, b, a = image.getpixel(position)
                R, G, B, A = image.getpixel(Position)
                image.putpixel(position, (R, G, B, A))
                image.putpixel(Position, (r, g, b, a))
            else:
                break
    log('bbb')

    return image
    # pass


def flop(image):
    """
    image 是一个 Image 对象

    不修改原图像
    返回一个 Image 对象, 它是 image 左右镜像的图像
    """
    width, height = image.size
    for i in range(width):
        for a in range(height):
            position = (i, a)
            Position = (width - i - 1, a)
            if i < width - i:
                r, g, b, a = image.getpixel(position)
                R, G, B, A = image.getpixel(Position)
                image.putpixel(position, (R, G, B, A))
                image.putpixel(Position, (r, g, b, a))
            else:
                break

    return image
    # pass


def main():
    """
    压缩包内有图片 a.jpg
    图片是面朝左的 doge 加下方的四个字
    要求生成一张图片 b.jpg, 狗头朝右但下方文字不变
    """
    img = Image.open('a.jpg')
    img = img.convert('RGBA')
    i = crop(img, (0, 0, 100, 97))
    i.show()
    i.save ('crop.png')
    # i = flip(img)
    # i.show()
    # i.save('flip.png')
    # i = flop(img)
    # i.show()
    # i.save('b.png')
    # pass



if __name__ == '__main__':
    main()
