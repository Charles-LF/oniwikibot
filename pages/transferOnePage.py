import re

from mwclient import Site

from img.img import transferImg
from sites import login


def transferPage(oldSite: Site, newSite: Site, pageName: str, username, password, sessiondata):
    replace_str = r'\[\[(en|ru|pt-br):[^\]]*\]\]'
    old_Site = login.login_to_wikigg(site=oldSite, username=username, password=password)
    new_Site = login.login_to_bwiki(site=newSite, sessiondata=sessiondata)

    oldSiteText = re.sub(replace_str, "", old_Site.pages[pageName].text())
    newSiteText = new_Site.pages[pageName].text()

    if oldSiteText == newSiteText:
        print("页面相同")
        return 0
    # 尝试将DEV命名空间下得模块转化
    if "Dev:" in oldSiteText:
        oldSiteText = re.sub("Dev:", "Module:Dev/", oldSiteText)
    # 图片判断
    if "File:" in pageName:
        transferImg(oldSite=oldSite, newSite=newSite, fileName=re.sub('File:', '', pageName))

    res = newSite.pages[pageName].edit(oldSiteText, summary="页面手动同步", bot=True)
    print(f"更新已完成{res}")
    return 0
