from mwclient import Site

from sites import login


def transferPage(oldSite: Site, newSite: Site, pageName: str, username, password, sessiondata):
    old_Site = login.login_to_wikigg(site=oldSite, username=username, password=password)
    new_Site = login.login_to_bwiki(site=newSite, sessiondata=sessiondata)

    oldSiteText = old_Site.pages[pageName].text()
    newSiteText = new_Site.pages[pageName].text()
    if oldSiteText == newSiteText:
        print("页面相同")
        return 0
    res = newSite.pages[pageName].edit(oldSite.pages[pageName].text(), summary="页面手动同步", bot=True)
    print(res)
    return 0
