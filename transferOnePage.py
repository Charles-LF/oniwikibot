import os

from pages.transferOnePage import transferPage
from sites.sites import bwiki, wikigg

wikigg_user_name = ''
wikigg_user_password = ''
bwiki_session_data = ''

if 'GITHUB_ACTIONS' in os.environ:
    wikigg_user_name = os.environ.get('WIKIGG_USER')
    wikigg_user_password = os.environ.get('WIKIGG_USER_PASSWORD')
    bwiki_session_data = os.environ.get("BWIKI_SESSION_DATA")

pageName = '电解器'
if __name__ == '__main__':
    transferPage(oldSite=wikigg, newSite=bwiki, pageName=pageName, username=wikigg_user_name, password=wikigg_user_password, sessiondata=bwiki_session_data)
