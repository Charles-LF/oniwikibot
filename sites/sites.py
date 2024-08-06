from mwclient import Site

user_agent = 'CharlesBot/0.0.1 (Charles@klei.vip)'

wikigg = Site(host='oxygennotincluded.wiki.gg',
              path="/zh/", clients_useragent=user_agent)

bwiki = Site(host='wiki.biligame.com', path="/oni/", clients_useragent=user_agent)

# fandom = Site(host="oxygennotincluded.fandom.com", path="/zh/", clients_useragent=user_agent)
