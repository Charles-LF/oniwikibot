import os
import re

import requests
from bs4 import BeautifulSoup
from mwclient import Site


def MissingImg(sessionData: str, oldSite: Site, newSite: Site):
    """
    检查缺失的图片并转存，临时使用
    :param sessionData: bwiki得Session
    :param oldSite: 来源站点 这里是gg
    :param newSite: 目标站点 这里是bwiki
    :return: null
    """
    # 临时使用
    url = "https://wiki.biligame.com/oni/index.php?title=%E7%89%B9%E6%AE%8A:%E9%9C%80%E8%A6%81%E7%9A%84%E6%96%87%E4%BB%B6&limit=500&offset=0"

    res = requests.get(url, cookies={'SESSDATA': sessionData})
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    # class_='special'
    special_ol = soup.find('ol', class_='special')

    # 遍历该<ol>下的所有<li>元素
    for li in special_ol.find_all('li'):
        first_a = li.find('a')
        # 拿到第一个标签的名字 类似：  文件:材料科学研究.png
        if first_a.text == "文件:Http://image.namedq.com/uploads/20190303/20/1551614448-fAvkVdETgm.jpg":
            pass
        fileName = re.sub("文件:", "", first_a.text)
        print(fileName)
        try:
            file = oldSite.images[fileName]

            with open(fileName, "wb") as f:
                file.download(f)

            with open(fileName, 'rb') as f:
                newSite.upload(f, filename=fileName, description="== 授权协议 ==\n{{游戏版权}}",
                               comment='文件缺失补全', ignore=True)
                print(f"上传文件: {fileName}")

        except Exception as e:
            print(e)
        finally:
            if os.path.exists(fileName):
                os.remove(fileName)
            
