import datetime
import re

from mwclient import Site

import user

user_agent = 'CharlesBot/0.0.1 (Charles@klei.vip)'
fandom = Site('oxygennotincluded.fandom.com', path="/zh/", clients_useragent=user_agent)
bwiki = Site('wiki.biligame.com', path="/oni/", clients_useragent=user_agent)
fandom.login(username=user.fadom_user_name, password=user.fadom_user_password)
bwiki.login(cookies={'SESSDATA': user.bwiki_session_data})

print(f"fandom登录:{fandom.logged_in}")
print(f"bwiki登录:{bwiki.logged_in}")


def replace_special_chars(input_string):
    # 定义 Windows 文件命名不允许使用的特殊字符
    special_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', 'File']

    # 替换特殊字符为 HTML 转义字符
    for char in special_chars:
        input_string = input_string.replace(char, "")

    return input_string


def update_pages(old_site: Site, new_site: Site):
    one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    end_time = one_day_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
    changes_list_old = old_site.get(action="query", list="recentchanges", rcend=end_time, rcdir="older",
                                    rcprop="user|comment|title|timestamp", rclimit=5)

    page = changes_list_old["query"]["recentchanges"]
    changes_title = []
    for item in page:
        print(changes_title)
        if item["title"] in changes_title:
            continue
        changes_title.append(item["title"])

        replace_str = r'\[\[(en|ru):[^\]]*\]\]'

        oldpage_text = re.sub(replace_str, "", old_site.pages[item["title"]].text())

        new_site_text = new_site.pages[item["title"]].text()
        if oldpage_text != new_site_text:
            res = new_site.pages[item["title"]].edit(oldpage_text,
                                                     summary=f'原站点{item["title"]}于{item["timestamp"]}由{item["user"]}更改,于此时同步')
            print(res)
