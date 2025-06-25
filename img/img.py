import io

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


def transferDiffImg(oldSite: Site, newSite: Site) -> None:
    """
    检查两个站点间的图片，将旧站存在但新站没有的图片转存至新站点
    :param oldSite: 原站点
    :param newSite: 镜像站点
    :return: None
    """
    # 收集新旧站点的所有图片名称集合
    old_img_names = {img.name.replace("文件:", "").replace("File:", "") for img in oldSite.allimages(generator=True)}
    new_img_names = {img.name.replace("文件:", "").replace("File:", "") for img in newSite.allimages(generator=True)}

    # 计算需要从旧站转移到新站的图片（仅旧站存在的）
    images_to_transfer = old_img_names - new_img_names

    if not images_to_transfer:
        print("没有需要转移的图片")
        return

    print(f"发现 {len(images_to_transfer)} 张图片需要转移")
    success_count = 0
    failed_images = []
    skipped_images = []  # 新增：记录跳过的图片

    for img_name in sorted(images_to_transfer):
        # 新增：检查图片扩展名，跳过.webp和.ico格式
        if img_name.lower().endswith(('.webp', '.ico')):
            skipped_images.append(img_name)
            print(f"跳过图片: {img_name} (不支持的格式)")
            continue

        try:
            print(f"正在处理图片: {img_name}")
            transferImg(oldSite, newSite, img_name)
            success_count += 1
        except Exception as e:
            failed_images.append((img_name, str(e)))
            print(f"错误: 无法转移图片 {img_name} - {e}")

    # 输出转移结果摘要
    print("\n===== 转移结果 =====")
    print(f"成功: {success_count} 张")
    print(f"失败: {len(failed_images)} 张")
    print(f"跳过: {len(skipped_images)} 张")  # 新增：输出跳过的图片数量

    if failed_images:
        print("\n失败的图片列表:")
        for name, error in failed_images:
            print(f"- {name}: {error}")

    if skipped_images:  # 新增：输出跳过的图片列表
        print("\n跳过的图片列表:")
        for name in skipped_images:
            print(f"- {name}")
