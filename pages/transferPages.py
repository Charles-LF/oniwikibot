import datetime
import random
import re
import time

from mwclient import Site

from img.img import transferImg

# 常量定义
CROSS_SITE_LINK_REGEX = r'\[\[(en|ru|pt-br):[^\]]*\]\]'
DEV_NAMESPACE_PREFIX = "Dev:"
MODULE_NAMESPACE_PREFIX = "Module:Dev/"
IGNORED_PAGES = ["教程"]
IMAGE_NAMESPACE_ID = 6


def clean_page_text(page_text: str) -> str:
    """清理页面文本中的跨站链接"""
    return re.sub(CROSS_SITE_LINK_REGEX, "", page_text)


def convert_dev_namespace(page_text: str) -> str:
    """将 Dev: 命名空间转换为 Module:Dev/"""
    return page_text.replace(DEV_NAMESPACE_PREFIX, MODULE_NAMESPACE_PREFIX)


def process_image(old_site: Site, new_site: Site, title: str):
    """处理图片页面的传输"""
    if "File:" in title and IMAGE_NAMESPACE_ID == 6:
        transferImg(oldSite=old_site, newSite=new_site, fileName=title)
        return True
    return False


def update_single_page(old_site: Site, new_site: Site, title: str, user: str):
    """更新单个页面"""
    try:
        print(f"正在处理 {title}")
        old_page_text = clean_page_text(old_site.pages[title].text())
        old_page_text = convert_dev_namespace(old_page_text)
        new_page_text = new_site.pages[title].text()

        if old_page_text != new_page_text:
            res = new_site.pages[title].edit(
                text=old_page_text,
                summary=f'原站点 {title} 由 {user} 更改, 于此时同步'
            )
            print(res)
    except Exception as e:
        print(f"处理页面 {title} 时出错: {e}")


def update_pages(old_site: Site, new_site: Site):
    """根据最近更改列表更新页面"""
    now = datetime.datetime.now()
    three_hours_ago = now - datetime.timedelta(hours=3)
    print(f"开始处理 {three_hours_ago} 到 {now} 的更新...")
    end_time = int(three_hours_ago.timestamp())

    changes_list_old = old_site.get(
        action="query",
        list="recentchanges",
        rcstart="now",
        rcend=end_time,
        rcdir="older",
        rcprop="user|comment|title|timestamp"
    )
    pages = changes_list_old["query"]["recentchanges"]
    processed_titles = set()

    for page in pages:
        title = page["title"]
        if title in IGNORED_PAGES:
            print(f"{title} 在无需处理的页面列表中, 跳过")
            continue
        if title in processed_titles:
            print(f"已经处理过 {title}, 跳过")
            continue
        if process_image(old_site, new_site, title):
            processed_titles.add(title)
            continue

        update_single_page(old_site, new_site, title, page["user"])
        processed_titles.add(title)


def transfer_all_pages(old_site: Site, new_site: Site):
    """同步两个站点的所有页面"""
    all_pages = list(old_site.allpages(generator=True))
    for page in all_pages:
        print(f"正在处理 {page.name}")
        time.sleep(random.uniform(1, 1.8))
        try:
            old_page_text = clean_page_text(old_site.pages[page.name].text())
            new_page = new_site.pages[page.name]
            new_page_text = new_page.text()

            if old_page_text != new_page_text:
                new_page.edit(
                    text=old_page_text,
                    summary="原站同步, 尝试清除外链.",
                    bot=True
                )
        except Exception as e:
            print(f"处理页面 {page.name} 时出错: {e}")
