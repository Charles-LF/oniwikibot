import datetime
import random
import re
import time

from mwclient import Site

from img.img import transferImg
from sites import login

replace_str = r'\[\[(en|ru|pt-br):[^\]]*\]\]'

# 把不需要处理的页面名称丢这里
donothing = ["教程"]


def update_pages(old_site: Site, new_site: Site, username, password, sessiondata):
    # 登录GG
    old_site = login.login_to_wikigg(old_site, username=username, password=password)

    # 获取当前时间
    now = datetime.datetime.now()
    # 计算3小时前的时间
    three_hours_ago = now - datetime.timedelta(hours=3)
    print(f"开始处理{three_hours_ago}到{now}的更新...")

    # 将时间转换为MediaWiki的时间戳格式（Unix时间戳）
    end_time = int(three_hours_ago.timestamp())

    # 获取更改列表
    changes_list_old = old_site.get(action="query", list="recentchanges", rcstart="now", rcend=end_time, rcdir="older", rcprop="user|comment|title|timestamp")
    pages = changes_list_old["query"]["recentchanges"]

    # 判断处理列表数量
    if len(pages) > 0:
        print(len(pages))
        new_site = login.login_to_bwiki(site=new_site, sessiondata=sessiondata)

    changes_title = []

    for page in pages:

        title = page["title"]
        try:
            print(f"正在处理{title}")
            if title in donothing:
                changes_title.append(title)
                print("在无需处理的页面列表中,跳过")
                continue
            if title in changes_title:
                print(f"已经处理过{title},跳过")
                continue

            # 图片判断
            if ("File:" in title) & (page["ns"] == 6):
                transferImg(oldSite=old_site, newSite=new_site, fileName=title)
                changes_title.append(title)
                continue

            # 尝试跨站底部链接清除
            oldpage_text = re.sub(replace_str, "", old_site.pages[title].text())

            # 尝试将DEV命名空间下得模块转化
            if "Dev:" in oldpage_text:
                oldpage_text = re.sub("Dev:", "Module:Dev/", oldpage_text)
            new_site_text = new_site.pages[title].text()

            if oldpage_text != new_site_text:
                res = new_site.pages[title].edit(oldpage_text, summary=f'原站点{title}由{page["user"]}更改,于此时同步')
                print(res)
            changes_title.append(title)
        except Exception as e:
            print(e)


def transferAllPages(oldSite: Site, newSite: Site):
    """
    同步两个站点的页面,使用allpages
    :param oldSite: 来源站点
    :param newSite: 目标站点
    :return: null
    """
    allpages = list(oldSite.allpages(generator=True))
    for page in allpages:
        print(f"正在处理{page.name}")
        time.sleep(random.uniform(1, 1.8))
        try:
            oldpage_text = re.sub(replace_str, "", oldSite.pages[page.name].text())
            newpage = newSite.pages[page.name]
            newpage_text = newpage.text()
            if oldpage_text != newpage_text:
                newpage.edit(text=oldpage_text, summary="原站同步,尝试清除外链.", bot=True)
        except Exception as e:
            print(e)
