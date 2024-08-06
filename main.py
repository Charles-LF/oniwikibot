import datetime
import os
import re

from mwclient import Site

from sites.sites import bwiki, wikigg

wikigg_user_name = ''
wikigg_user_password = ''
bwiki_session_data = ''

if 'GITHUB_ACTIONS' in os.environ:
    wikigg_user_name = os.environ.get('WIKIGG_USER')
    wikigg_user_password = os.environ.get('WIKIGG_USER_PASSWORD')
    bwiki_session_data = os.environ.get("BWIKI_SESSION_DATA")

wikigg.login(username=wikigg_user_name, password=wikigg_user_password)
bwiki.login(cookies={'SESSDATA': bwiki_session_data})

print(f"wikigg登录:{wikigg.logged_in}")
print(f"bwiki登录:{bwiki.logged_in}")


# fandom.login(username=wikigg_user_name, password=wikigg_user_password)


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


update_pages(wikigg, bwiki)
