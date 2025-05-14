import io
import random
import time

from mwclient import Site


def transferImg(oldSite: Site, newSite: Site, fileName: str, comment: str = '原站文件上传同步', ignore: bool = False) -> None:
    """
    转存单个图片文件。
    :param oldSite: 来源站点
    :param newSite: 目标站点
    :param fileName: 文件名，例如：File:测试.png
    :param comment: 上传注释
    :param ignore: 是否忽略警告
    """
    image_name = fileName.replace("File:", "")
    try:
        file = oldSite.images[image_name]
        # 使用 BytesIO 处理图片内容
        file_content = file.download()
        file_obj = io.BytesIO(file_content)

        # 上传图片
        newSite.upload(
            file=file_obj,
            filename=image_name,
            description="== 授权协议 ==\n{{游戏版权}}",
            comment=comment,
            ignore=ignore
        )
        print(f"成功上传图片: {image_name}")

    except Exception as e:
        print(f"转存失败: {e}")


def transferAllImg(oldSite: Site, newSite: Site) -> None:
    """
    批量转存所有图片文件。
    :param oldSite: 来源站点
    :param newSite: 目标站点
    """
    all_images_list = list(oldSite.allimages(generator=True))
    for image in all_images_list:
        time.sleep(random.uniform(1, 1.5))
        fileName = "File:" + image.name
        print(f"正在处理: {fileName}")
        transferImg(oldSite, newSite, fileName, comment='机器人批量上传', ignore=True)
