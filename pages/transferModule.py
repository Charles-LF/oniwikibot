from mwclient import Site

from sites import login

moduleListStr = ['Data', 'I18n']


def transModule(oldSite: Site, newSite: Site,username,password,sessiondata):
    """
    临时使用的模块转存
    :param oldSite: 这要填GG
    :param newSite: 新站点是bWiki
    :param sessiondata: sessiondata
    :param password: password
    :param username: username
    :return: null
    """
    moduleList = []  # 等着要处理的列表

    namespace_number = 828  # 神tm 828,找半天
    # 登录GG
    oldSite = login.login_to_wikigg(oldSite, username=username, password=password)
    # 登录bwiki
    newSite = login.login_to_bwiki(site=newSite, sessiondata=sessiondata)

    # 拿到模块命名空间下的所有子模块
    namespace_prefix = oldSite.namespaces[namespace_number]
    for page in oldSite.allpages(namespace=namespace_number):

        title = page.name
        if title.startswith(namespace_prefix + ':'):
            pageTitle = title[len(namespace_prefix) + 1:]
            for prefix in moduleListStr:
                # 将要同步的模块从茫茫模块中挑选出来丢到上面的列表里边在处理
                if pageTitle.startswith(prefix) and pageTitle not in moduleList:
                    moduleList.append(pageTitle)
                    # print(pageTitle)
    for module in moduleList:
        module = "Module:" + module  # 拿到要处理的页面名称
        # newSite  是bwiki
        newText = newSite.pages[module].text()
        oldText = oldSite.pages[module].text()
        if oldText != newText:
            res = newSite.pages[module].edit(text=oldText, summary="原站模块同步")
            print(res)
