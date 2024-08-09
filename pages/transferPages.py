import datetime
import random
import re
import time

from mwclient import Site

from img.img import transferImg

replace_str = r'\[\[(en|ru|pt-br):[^\]]*\]\]'


def update_pages(old_site: Site, new_site: Site):
    """
    通过最近更改同步两个站点之间的内容
    :param old_site: 来源站
    :param new_site: 目标站
    :return: null
    """
    one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    end_time = one_day_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
    changes_list_old = old_site.get(action="query", list="recentchanges", rcend=end_time,
                                    rcdir="older", rcprop="user|comment|title|timestamp", rclimit=20)

    page = changes_list_old["query"]["recentchanges"]
    changes_title = []
    for item in page:
        try:
            print(f"正在处理{item["title"]}")
            if item["title"] in changes_title:
                continue

            # 图片判断
            if ("File:" in item["title"]) & (item["ns"] == 6):
                transferImg(oldSite=old_site, newSite=new_site, fileName=item["title"])
                continue

            changes_title.append(item["title"])

            # 尝试跨站底部链接清除
            oldpage_text = re.sub(replace_str, "", old_site.pages[item["title"]].text())
            # 尝试将DEV命名空间下得模块转化
            if "Dev:" in oldpage_text:
                oldpage_text = re.sub("Dev:", " Module:Dev/", oldpage_text)
            new_site_text = new_site.pages[item["title"]].text()

            if oldpage_text != new_site_text:
                res = new_site.pages[item["title"]].edit(oldpage_text, summary=f'原站点{item["title"]}于{item["timestamp"]}由{item["user"]}更改,于此时同步')
                print(res)
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
