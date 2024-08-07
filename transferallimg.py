import os

from img.img import transferAllImg
from sites.sites import bwiki, wikigg

wikigg_user_name = ''
wikigg_user_password = ''
bwiki_session_data = ''

if 'GITHUB_ACTIONS' in os.environ:
    wikigg_user_name = os.environ.get('WIKIGG_USER')
    wikigg_user_password = os.environ.get('WIKIGG_USER_PASSWORD')
    bwiki_session_data = os.environ.get("BWIKI_SESSION_DATA")

if __name__ == '__main__':
    wikigg.login(username=wikigg_user_name, password=wikigg_user_password)
    bwiki.login(cookies={'SESSDATA': bwiki_session_data})

    print(f"wikigg登录:{wikigg.logged_in}")
    print(f"bwiki登录:{bwiki.logged_in}")

    transferAllImg(wikigg, bwiki)
