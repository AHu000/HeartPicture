from PIL import Image
import os
import math
import random
import uuid

# 处理的所有图片及结果存放的总目录
dir = "F:/PythonFile/HeartPicture/Picture"

# 白底图片所在的路径
whiteImagePath = ["F:/PythonFile/HeartPicture/WhiteFolded/White.jpg"]

# 白底图片所在的目录
whiteGoalPath = "F:/PythonFile/HeartPicture/WhiteFolded"

# 拼接后的图片的总尺寸，根据尺寸和图片数量计算出每张图片的大小
totalSize = 1000

# 重设大小后的图片所在的目录
transferDir = 'F:/PythonFile/HeartPicture/1/'

# 拼接结果图片所在的目录
resultDir = 'F:/PythonFile/HeartPicture/2/'


# 计算每个拼接大图需要多少个小图作为边长拼接
def getSize(num):
    # 最小边长从5开始，由其心形规律得出n的计算公式（推理步骤不放出来了）
    n = math.floor(math.sqrt(2 * num + 27 / 4) - 1.5)
    # 若为偶数，则减一
    if n % 2 == 0:
        n -= 1
    return n


# 获取指定路径下的所有图片
def getImagesName(dir):
    allPicPath = []  # 所有图片
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
                allPicPath.append(dir + '/' + file)
    return allPicPath


# 将图片转化为指定大小
def transferSize(allPicPath, height, width, goalPath):
    for i in range(len(allPicPath)):
        im = Image.open(allPicPath[i])
        out = im.resize((height, width), Image.ANTIALIAS)
        out.save(goalPath + str((allPicPath[i].split('/')[len(allPicPath[i].split('/')) - 1])))


def main(dir):
    # 获取所有指定目录下所有图片的路径
    allPicPath = getImagesName(dir)
    # 得到图片数量
    numOfPic = len(allPicPath)

    # 获取生成图片的边长大小，并计算出每个图片的边长应该是多大
    size = getSize(numOfPic)
    height = math.floor(totalSize / size)
    width = math.floor(totalSize / size)

    # 将用于拼接的图片都格式化为统一大小的图片
    transferSize(allPicPath, height, width, transferDir)
    # 获取所有格式化后的拼接图片的路径
    allTransPicPath = getImagesName(transferDir)

    # 获取用于填充多余部分的格式化后的白色图片的image
    # transferSize(whiteImagePath, height, width, whiteGoalPath[0])

    # perPicNum = math.floor(math.sqrt(numOfPic))
    toImage = Image.new('RGBA', (totalSize, totalSize))

    # 随机打乱用于拼接的图片的顺序，这样可保证每次拼接出来的图片顺序都是不同的
    random.shuffle(allTransPicPath)

    # 用于统计使用的拼图的图的数量
    j = 0
    print(len(allTransPicPath))

    # 获取白底图片的image，并设置好同样大小备用
    im = Image.open(whiteImagePath[0])
    out = im.resize((height, width), Image.ANTIALIAS)

    m = 1

    # 给每行分页粘贴size个小图片
    for i in range(size):
        if i == 0:
            k = 0
            # 打印一个空白格
            loc = ((k % size) * width, (int(i % size) * height))
            print(loc)
            toImage.paste(out, loc)
            k += 1

            # 打印一个图案
            loc = ((k % size) * width, (int(i % size) * height))
            print(loc)
            fromImage = Image.open(allTransPicPath[j])
            j += 1
            toImage.paste(fromImage, loc)
            k += 1

            # 打印 （size-4） 个空白格
            for h in range(size - 4):
                loc = ((k % size) * width, (int(i % size) * height))
                print(loc)
                toImage.paste(out, loc)
                k += 1

            # 打印一个图案
            loc = ((k % size) * width, (int(i % size) * height))
            print(loc)
            fromImage = Image.open(allTransPicPath[j])
            j += 1
            toImage.paste(fromImage, loc)
            k += 1

            # 打印一个空白格
            loc = ((k % size) * width, (int(i % size) * height))
            print(loc)
            toImage.paste(out, loc)
            k += 1

        elif i <= (size - 3) / 2 - 1 and i > 0:
            k = 0
            # 根据规律，先打印 i+2 个图片
            for s in range(i + 2):
                loc = ((k % size) * width, (int(i % size) * height))
                print(loc)
                fromImage = Image.open(allTransPicPath[j])
                j += 1
                toImage.paste(fromImage, loc)
                k += 1
            # 然后打印 （size-（i+2）*2）个空白格
            for h in range(size - (i + 2) * 2):
                loc = ((k % size) * width, (int(i % size) * height))
                print(loc)
                toImage.paste(out, loc)
                k += 1
            # 最后再打印 （i+2）个图片
            for s in range(i + 2):
                loc = ((k % size) * width, (int(i % size) * height))
                print(loc)
                fromImage = Image.open(allTransPicPath[j])
                j += 1
                toImage.paste(fromImage, loc)
                k += 1
        elif i > (size - 3) / 2 - 1 and i <= (size - 3) / 2 + 1:
            # i在满足条件的范围内打印（size）个图片
            for k in range(size):
                loc = ((k % size) * width, (int(i % size) * height))
                print(loc)
                fromImage = Image.open(allTransPicPath[j])
                j += 1
                toImage.paste(fromImage, loc)
        else:
            k = 0
            for x in range(m):
                loc = ((k % size) * width, (int(i % size) * height))
                print(loc)
                toImage.paste(out, loc)
                k += 1
            for y in range(size - 2 * m):
                loc = ((k % size) * width, (int(i % size) * height))
                print(loc)
                fromImage = Image.open(allTransPicPath[j])
                j += 1
                toImage.paste(fromImage, loc)
                k += 1
            for x in range(m):
                loc = ((k % size) * width, (int(i % size) * height))
                print(loc)
                toImage.paste(out, loc)
                k += 1
            m += 1
    # 在将所有的图片都粘贴到大画布后将合成图保存到指定目录下，并随机分配一个名字
    toImage.save(resultDir + str(uuid.uuid4()) + '.png')


if __name__ == '__main__':
    main(dir)
