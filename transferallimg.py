from img.img import transferAllImg
from sites.sites import bwiki_site, wikigg_site

if __name__ == '__main__':
    print(f"wikigg登录:{wikigg_site.logged_in}")
    print(f"bwiki登录:{bwiki_site.logged_in}")

    transferAllImg(wikigg_site, bwiki_site)
