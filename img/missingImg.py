import io
import re

import requests
from bs4 import BeautifulSoup
from mwclient import Site


def missing_img(session_data: str, old_site: Site, new_site: Site):
    """

    """
    # 临时使用
    url = "https://wiki.biligame.com/oni/index.php?title=%E7%89%B9%E6%AE%8A:%E9%9C%80%E8%A6%81%E7%9A%84%E6%96%87%E4%BB%B6&limit=500&offset=0"

    res = requests.get(url, cookies={'SESSDATA': session_data})
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    # class_='special'
    special_image_list = soup.find('ol', class_='special')

    # 遍历该<ol>下的所有<li>元素
    for li in special_image_list.find_all('li'):
        first_image_link = li.find('a')
        # 拿到第一个标签的名字 类似：  文件:材料科学研究.png
        if first_image_link.text == "文件:Http://image.namedq.com/uploads/20190303/20/1551614448-fAvkVdETgm.jpg":
            pass
        fileName = re.sub("文件:", "", first_image_link.text)
        print(fileName)
        try:
            file = old_site.images[fileName]

            # 使用 BytesIO 处理图片内容
            file_content = file.download()
            file_obj = io.BytesIO(file_content)

            # 上传图片
            new_site.upload(
                file=file_obj,
                filename=fileName,
                description="== 授权协议 ==\n{{游戏版权}}",
                comment='文件缺失补全',
                ignore=True
            )
            print(f"成功上传图片: {fileName}")

        except Exception as e:
            print(f"处理图片 {fileName} 时出错: {e}")
