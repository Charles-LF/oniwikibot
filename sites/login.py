import time

from mwclient import Site


def login_to_bwiki(site: Site, sessiondata, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            site.login(cookies={'SESSDATA': sessiondata})
            if site.logged_in:
                print("BWIKI登录成功思密达！！！")
                return site
        except Exception as e:
            print(f"登录次数 {attempts + 1} 失败: {e}")
            attempts += 1
            time.sleep(10)
    print("多次登录失败，请检查")


def login_to_wikigg(site: Site, username, password, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            site.login(username=username, password=password)
            if site.logged_in:
                print("GG登录成功思密达！！！")
                return site
        except Exception as e:
            print(f"登录次数 {attempts + 1} 失败: {e}")
            attempts += 1
            time.sleep(5)
    print("多次登录失败，请检查")
