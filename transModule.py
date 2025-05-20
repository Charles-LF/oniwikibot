from pages.transferModule import trans_module
from sites.sites import wikigg_site, bwiki_site

if __name__ == '__main__':
    trans_module(old_site=wikigg_site, new_site=bwiki_site)
