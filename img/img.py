import os
import re
import string

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
                           comment='原站图片上传同步', ignore=True)
            print(f"上传文件: {fileName}")
        os.remove(fileName)

    except Exception as e:
        os.remove(fileName)
        print(e)
