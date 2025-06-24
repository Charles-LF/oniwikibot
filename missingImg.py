from img.img import transferDiffImg
from sites.sites import wikigg_site, bwiki_site

if __name__ == '__main__':
    transferDiffImg(oldSite=wikigg_site, newSite=bwiki_site)
