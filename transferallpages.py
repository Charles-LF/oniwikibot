from pages.transferPages import transfer_all_pages
from sites.sites import wikigg_site, bwiki_site

if __name__ == '__main__':
    print(f"wikigg登录:{wikigg_site.logged_in}")
    print(f"bwiki登录:{bwiki_site.logged_in}")
    transfer_all_pages(old_site=wikigg_site, new_site=bwiki_site)
