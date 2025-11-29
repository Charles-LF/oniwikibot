import os
import sys

from mwclient import Site

user_agent = 'CharlesBot/0.0.2 (Charles@klei.vip)'
wikigg_user_name = 'LfBot'
wikigg_user_password = ''
bwiki_session_data = ''
huiji_user_name = 'Ra hua@CharlesBot'
huiji_user_password = ''
uakey = ''

if 'GITHUB_ACTIONS' in os.environ:
    wikigg_user_name = os.environ.get('WIKIGG_USER')
    wikigg_user_password = os.environ.get('WIKIGG_USER_PASSWORD')
    bwiki_session_data = os.environ.get("BWIKI_SESSION_DATA")
    huiji_user_name = os.environ.get("HUIJI_USER")
    huiji_user_password = os.environ.get("HUIJI_USER_PASSWORD")
    uakey = os.environ.get("UAKEY")

wikigg_site = Site(host='oxygennotincluded.wiki.gg', path="/zh/", clients_useragent=user_agent)
bwiki_site = Site(host='wiki.biligame.com', path="/oni/", clients_useragent=user_agent)
huiji_site = Site(host='oni.huijiwiki.com', clients_useragent=user_agent, custom_headers={'X-authkey': uakey})
# fandom = Site(host="oxygennotincluded.fandom.com", path="/zh/", clients_useragent=user_agent)


wikigg_site.login(username=wikigg_user_name, password=wikigg_user_password)
bwiki_site.login(cookies={'SESSDATA': bwiki_session_data})
huiji_site.login(username=huiji_user_name, password=huiji_user_password)

if not bwiki_site.logged_in:
    sys.exit('bwiki session 登录状态异常')
if not wikigg_site.logged_in:
    sys.exit('wiki gg 登录状态异常')
