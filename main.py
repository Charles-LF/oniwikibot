from pages.transferPages import update_pages
from sites.sites import wikigg_site, bwiki_site, huiji_site

if __name__ == '__main__':
    update_pages(old_site=wikigg_site, new_site=bwiki_site)
    update_pages(old_site=wikigg_site, new_site=huiji_site)
