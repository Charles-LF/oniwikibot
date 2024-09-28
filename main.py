import os
import sys

from pages.transferPages import update_pages
from sites.sites import bwiki, wikigg, login_to_wiki

wikigg_user_name = ''
wikigg_user_password = ''
bwiki_session_data = ''

if 'GITHUB_ACTIONS' in os.environ:
    wikigg_user_name = os.environ.get('WIKIGG_USER')
    wikigg_user_password = os.environ.get('WIKIGG_USER_PASSWORD')
    bwiki_session_data = os.environ.get("BWIKI_SESSION_DATA")

if __name__ == '__main__':
    login_bwiki = login_to_wiki(bwiki, sessiondata=bwiki_session_data)
    wikigg.login(username=wikigg_user_name, password=wikigg_user_password)

    print(f"wikigg登录:{wikigg.logged_in}")
    print(f"bwiki登录:{login_bwiki.logged_in}")

    # 检测bwiki登录状态，没登陆说明session过期了
    if not bwiki.logged_in:
        sys.exit(1)

    update_pages(wikigg, login_bwiki)
