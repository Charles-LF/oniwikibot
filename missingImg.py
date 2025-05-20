import re
from typing import List

from bs4 import BeautifulSoup
from mwclient import Site

from img.img import transferImg
from sites.sites import bwiki_site, bwiki_session_data, wikigg_site

# 常量定义
MISSING_IMAGES_URL = "https://wiki.biligame.com/oni/index.php?title=%E7%89%B9%E6%AE%8A:%E9%9C%80%E8%A6%81%E7%9A%84%E6%96%87%E4%BB%B6&limit=500&offset=0"
FILE_PREFIX = "文件:"


def fetch_missing_image_names(session_data: str) -> List[str]:
    """
    从指定 URL 抓取缺失图片的文件名列表。
    :param session_data: 用于认证的 SESSDATA
    :return: 缺失图片的文件名列表
    """
    import requests
    res = requests.get(MISSING_IMAGES_URL, cookies={'SESSDATA': session_data})
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    special_image_list = soup.find('ol', class_='special')
    if not special_image_list:
        return []
    image_names = [
        re.sub(FILE_PREFIX, "", li.find('a').text)
        for li in special_image_list.find_all('li')
        if li.find('a') and li.find('a').text.startswith(FILE_PREFIX)
    ]
    return image_names


def process_missing_images(image_names: List[str], old_site: Site, new_site: Site):
    """
    处理缺失图片，执行下载和上传操作。
    :param image_names: 缺失图片的文件名列表
    :param old_site: 来源站点
    :param new_site: 目标站点
    """
    for file_name in image_names:
        try:
            transferImg(
                oldSite=old_site,
                newSite=new_site,
                fileName=f"File:{file_name}",
                comment='文件缺失补全',
                ignore=True
            )
        except Exception as e:
            print(f"处理图片 {file_name} 时出错: {e}")


def missing_img(session_data: str, old_site: Site, new_site: Site):
    """
    主函数，负责协调缺失图片的抓取和处理。
    :param session_data: 用于认证的 SESSDATA
    :param old_site: 来源站点
    :param new_site: 目标站点
    """
    # 抓取缺失图片的文件名
    missing_image_names = fetch_missing_image_names(session_data)
    if not missing_image_names:
        print("未找到缺失图片")
        return
    # 处理缺失图片
    process_missing_images(missing_image_names, old_site, new_site)
    print("处理完成")


if __name__ == '__main__':
    missing_img(session_data=bwiki_session_data, old_site=wikigg_site, new_site=bwiki_site)
