import re

from mwclient import Site

from img.img import transferImg

# 提取常量
REPLACE_STR = r'\[\[(en|ru|pt-br):[^\]]*\]\]'
DEV_NAMESPACE_OLD = "Dev:"
DEV_NAMESPACE_NEW = "Module:Dev/"


def clean_page_text(text: str) -> str:
    """清理页面文本，移除指定的正则匹配内容"""
    return re.sub(REPLACE_STR, "", text)


def convert_dev_namespace(text: str) -> str:
    """将 Dev: 命名空间转换为 Module:Dev/"""
    return text.replace(DEV_NAMESPACE_OLD, DEV_NAMESPACE_NEW)


def handle_image_transfer(old_site: Site, new_site: Site, page_name: str):
    """处理图片传输"""
    if "File:" in page_name:
        file_name = page_name.replace("File:", "")
        transferImg(
            oldSite=old_site,
            newSite=new_site,
            fileName=file_name,
            comment="原站文件上传同步"
        )


def edit_page(new_site: Site, page_name: str, content: str):
    """编辑新站点页面"""
    try:
        res = new_site.pages[page_name].edit(
            content,
            summary="页面手动同步",
            bot=True
        )
        print(f"更新已完成: {res}")
    except Exception as e:
        print(f"更新页面失败: {e}")


def transferPage(old_site: Site, new_site: Site, page_name: str):
    # 获取并清理页面文本
    old_site_text = clean_page_text(old_site.pages[page_name].text())
    new_site_text = new_site.pages[page_name].text()

    # 检查页面是否相同
    if old_site_text == new_site_text:
        print("页面相同")
        return

    # 转换 Dev 命名空间
    old_site_text = convert_dev_namespace(old_site_text)

    # 处理图片
    handle_image_transfer(old_site, new_site, page_name)

    # 编辑新站点页面
    edit_page(new_site, page_name, old_site_text)
