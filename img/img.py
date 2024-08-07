import os
import random
import re
import string
import time

from mwclient import Site


def transferImg(oldSite: Site, newSite: Site, fileName: string):
    """
    转存图片,实现好像很煞笔，但是能用
    :param oldSite: 来源站点
    :param newSite:  目标站点
    :param fileName:  文件名称，可以是 File:测试.png
    :return: null
    """
    try:
        fileName = re.sub("File:", "", fileName)
        file = oldSite.images[fileName]

        with open(fileName, "wb") as f:
            file.download(f)

        with open(fileName, 'rb') as f:
            newSite.upload(f, filename=fileName, description="== 授权协议 ==\n{{游戏版权}}",
                           comment='原站文件上传同步', ignore=True)
            print(f"上传文件: {fileName}")

    except Exception as e:
        print(e)
    finally:
        os.remove(fileName)


def transferAllImg(oldSite: Site, newSite: Site):
    """
    转存所有图片
    :param oldSite: 来源（旧）站点
    :param newSite: 目标（新）站点
    :return: null
    """
    allImgList = list(oldSite.allimages(generator=True))
    for img in allImgList:
        time.sleep(random.uniform(1, 1.5))
        fileName = img.name[5:]
        print(f"正在处理{fileName}")
        imgName = re.sub('"', "", fileName)
        try:
            file = oldSite.images[fileName]
            with open(imgName, "wb") as f:
                file.download(f)
            with open(imgName, "rb") as f:
                newSite.upload(f, filename='WIKI上的文件名', description="== 授权协议 ==\n{{游戏版权}}",
                               comment='机器人批量上传')
        except Exception as e:
            print(e)
        finally:
            os.remove(imgName)
