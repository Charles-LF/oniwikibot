import sys
import time

import mwclient
from mwclient import Site

user_agent = 'CharlesBot/0.0.1 (Charles@klei.vip)'

wikigg = Site(host='oxygennotincluded.wiki.gg',
              path="/zh/", clients_useragent=user_agent)

bwiki = Site(host='wiki.biligame.com', path="/oni/", clients_useragent=user_agent)


# fandom = Site(host="oxygennotincluded.fandom.com", path="/zh/", clients_useragent=user_agent)

def login_to_wiki(site: Site, sessiondata, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            site.login(cookies={'SESSDATA': sessiondata})
            if site.logged_in:
                print("登录成功思密达！！！")
                return site
        except mwclient.errors.LoginError as e:
            print(f"登录次数 {attempts + 1} 失败: {e}")
            attempts += 1
            time.sleep(5)  # Wait for 2 seconds before retrying
    print("多次登录失败，请检查")
