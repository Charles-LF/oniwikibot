import os
from pages.transferModule import transModule
from sites.sites import bwiki, wikigg

wikigg_user_name = ''
wikigg_user_password = ''
bwiki_session_data = ''

if 'GITHUB_ACTIONS' in os.environ:
    wikigg_user_name = os.environ.get('WIKIGG_USER')
    wikigg_user_password = os.environ.get('WIKIGG_USER_PASSWORD')
    bwiki_session_data = os.environ.get("BWIKI_SESSION_DATA")

if __name__ == '__main__':
    transModule(oldSite=wikigg,newSite=bwiki,username=wikigg_user_name,password=wikigg_user_password,sessiondata=bwiki_session_data)
