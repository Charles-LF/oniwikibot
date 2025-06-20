from pages.transferOnePage import transferPage
from sites.sites import bwiki_site, wikigg_site

pageName = '液桶抽出器'

if __name__ == '__main__':
    transferPage(old_site=wikigg_site, new_site=bwiki_site, page_name=pageName)
