import datetime
import re

from mwclient import Site

from img.img import transferImg


def update_pages(old_site: Site, new_site: Site):
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

            changes_title.append(item["title"])

            # 图片判断
            if ("File:" in item["title"]) & (item["ns"] == 6):
                transferImg(oldSite=old_site, newSite=new_site, fileName=item["title"])
                continue

            replace_str = r'\[\[(en|ru):[^\]]*\]\]'

            oldpage_text = re.sub(
                replace_str, "", old_site.pages[item["title"]].text())

            new_site_text = new_site.pages[item["title"]].text()

            if oldpage_text != new_site_text:
                res = new_site.pages[item["title"]].edit(oldpage_text,
                                                         summary=f'原站点{item["title"]}于{item["timestamp"]}由{item["user"]}更改,于此时同步')
                print(res)
        except Exception as e:
            print(e)
