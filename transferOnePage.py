from pages.transferOnePage import transferPage
from sites.sites import bwiki_site, wikigg_site

pageName = ['蛋']

if __name__ == '__main__':
    for name in pageName:
        transferPage(old_site=wikigg_site, new_site=bwiki_site, page_name=name)
