import os
import sys

import requests.exceptions
from mwclient import Site

user_agent = 'CharlesBot/0.0.2 (Charles@klei.vip)'
wikigg_user_name = 'LfBot'
wikigg_user_password = ''
bwiki_session_data = ''
huiji_user_name = 'Ra hua@CharlesBot'
huiji_user_password = ''
uakey = ''
loginTime = 1

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

def login():
    wikigg_site.login(username=wikigg_user_name, password=wikigg_user_password)
    bwiki_site.login(cookies={'SESSDATA': bwiki_session_data})
    huiji_site.login(username=huiji_user_name, password=huiji_user_password)


try:
    print(f"尝试登录第{loginTime}次")
    login()
except requests.exceptions.ConnectTimeout:
    print("连接超时，重试中。。。")
    loginTime += 1
    login()
except Exception as e:
    print(f"发生了错误：{type(e).__name__} - {e}")
    sys.exit(1)
if loginTime >= 4:
    sys.exit("登录次数过多，已结束进程")

if not bwiki_site.logged_in:
    sys.exit('bwiki session 登录状态异常')
if not wikigg_site.logged_in:
    sys.exit('wiki gg 登录状态异常')
