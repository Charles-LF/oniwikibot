from pages.transferPages import update_pages
from sites.sites import wikigg_site, bwiki_site, huiji_site

if __name__ == '__main__':
    print(f'GG登录情况：{wikigg_site.logged_in}')
    print(f'Bwiki登录情况：{bwiki_site.logged_in}')
    print(f'灰机登录情况：{huiji_site.logged_in}')
    update_pages(old_site=wikigg_site, new_site=bwiki_site)
    update_pages(old_site=wikigg_site, new_site=huiji_site)
