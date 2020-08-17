from PIL import Image

import math

log = print


def rorate_left(image):
    """
    image 是一个 Image 对象
    返回一个全新图像，它是 image 左转 90 度后的图像
    """
    width, height = image.size
    Imagenew = Image.new('RGBA', (height + 5, width + 5), 'white')
    # Imagenew.save(r'C:\Users\yangf\Documents\Tencent Files\513655976\FileRecv\项目3-图像旋转\new.png')
    for x in range(width):
        for y in range(height):
            position = (x, y)
            r, g, b, a = image.getpixel(position)
            x0 = width / 2
            y0 = height / 2
            xi = - x0 + x
            yi = - y0 + y
            xI = xi * math.cos(math.pi / 2) + yi * math.sin(math.pi / 2)
            yI = - xi * math.sin(math.pi / 2) + yi * math.cos(math.pi / 2)
            xo = int(xI + x0)
            yo = int(yI + y0)
            # log('the,number', xo, yo)
            # log('aaa')
            position = (xo, yo)
            Imagenew.putpixel(position,(r, g, b, a))


    return Imagenew


def rorate_right(image):
    """
    image 是一个 Image 对象
    返回一个全新图像，它是 image 右转 90 度后的图像
    """
    a = rorate_180(image)
    a = rorate_left(a)
    # pass
    return a


def rorate_180(image):
    """
    image 是一个 Image 对象
    返回一个全新图像，它是 image 旋转 180 度后的图像
    """
    a = rorate_left(image)
    a = rorate_left(a)
    # pass
    return a


def main():

    img = Image.open('a.jpg')
    img = img.convert('RGBA')
    i = rorate_left(img)
    i.show()
    i.save('crop.png')
    i = rorate_right(img)
    i.show()
    i.save('flip.png')
    i = rorate_180(img)
    i.show()
    i.save('b.png')


if __name__ == '__main__':
    main()