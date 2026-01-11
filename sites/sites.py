import os
import sys

import requests.exceptions
from mwclient import Site

USER_AGENT = 'CharlesBot/0.0.2 (Charles@klei.vip)'
WIKIGG_USER = 'LfBot'
DEFAULT_WIKIGG_PWD = ''
DEFAULT_BWIKI_SESSION = ''
DEFAULT_HUIJI_USER = 'Ra hua@CharlesBot'
DEFAULT_HUIJI_PWD = ''
DEFAULT_UAKEY = ''

MAX_LOGIN_RETRY = 3
login_retry_count = 1

# 从环境变量加载密钥（适配GITHUB_ACTIONS）
wikigg_user_name = os.environ.get('WIKIGG_USER', WIKIGG_USER)
wikigg_user_password = os.environ.get('WIKIGG_USER_PASSWORD', DEFAULT_WIKIGG_PWD)
bwiki_session_data = os.environ.get("BWIKI_SESSION_DATA", DEFAULT_BWIKI_SESSION)
huiji_user_name = os.environ.get("HUIJI_USER", DEFAULT_HUIJI_USER)
huiji_user_password = os.environ.get("HUIJI_USER_PASSWORD", DEFAULT_HUIJI_PWD)
uakey = os.environ.get("UAKEY", DEFAULT_UAKEY)

wikigg_site = Site(host='oxygennotincluded.wiki.gg', path="/zh/", clients_useragent=USER_AGENT)
bwiki_site = Site(host='wiki.biligame.com', path="/oni/", clients_useragent=USER_AGENT)
huiji_site = Site(host='oni.huijiwiki.com', clients_useragent=USER_AGENT, custom_headers={'X-authkey': uakey})


def wiki_login():
    """ 登录站点 """
    wikigg_site.login(username=wikigg_user_name, password=wikigg_user_password)
    bwiki_site.login(cookies={'SESSDATA': bwiki_session_data})  # bwiki是session cookie登录
    huiji_site.login(username=huiji_user_name, password=huiji_user_password)


while login_retry_count <= MAX_LOGIN_RETRY:
    try:
        print(f"尝试登录第 {login_retry_count} 次")
        wiki_login()
        print("✅ 站点全部登录成功！")
        break  # 登录成功，跳出重试循环
    except requests.exceptions.ConnectTimeout:
        # 捕获连接超时异常
        print(f"❌ 连接超时！剩余重试次数: {MAX_LOGIN_RETRY - login_retry_count}")
        login_retry_count += 1
    except Exception as e:
        # 捕获所有其他异常，不可重试，直接退出
        print(f"❌ 登录发生致命错误 [{type(e).__name__}]：{str(e)}")
        sys.exit(1)
else:
    # while循环正常结束 = 重试次数用尽仍失败
    print(f"❌ 登录重试{MAX_LOGIN_RETRY}次全部失败，终止进程")
    sys.exit(1)

# 校验登录状态
login_check_flag = True
if not bwiki_site.logged_in:
    print("❌ bwiki 站点登录状态异常，未成功登录")
    login_check_flag = False
if not wikigg_site.logged_in:
    print("❌ wikigg 站点登录状态异常，未成功登录")
    login_check_flag = False
if not huiji_site.logged_in:
    print("❌ huiji 站点登录状态异常，未成功登录")
    login_check_flag = False

# 状态校验失败则退出进程
if not login_check_flag:
    sys.exit(1)

# 导出站点实例
__all__ = ["wikigg_site", "bwiki_site", "huiji_site"]
