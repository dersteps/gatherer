# -*- coding: utf-8 -*-
import csv
import requests
import urllib
from pyquery import PyQuery as pq
import pprint

editions= {}
editions["LEA"] = "Alpha"
editions["LEB"] = "Beta"
editions["2ED"] = "Unlimited"
editions["CED"] = "Collectors%27+Edition"
editions["ARN"] = "Arabian Nights"
editions["PDRC"] = "Dragon Con"
editions["ATQ"] = "Antiquities"
editions["3ED"] = "Revised Edition"
editions["LEG"] = "Legends"
editions["SUM"] = "Summer Magic"
editions["DRK"] = "The Dark"
editions["FEM"] = "Fallen Empires"
editions["4ED"] = "Fourth Edition"
editions["ICE"] = "Ice Age"
editions["CHR"] = "Chronicles"
editions["REN"] = "Renaissance"
editions["HML"] = "Homelands"
editions["ALL"] = "Alliances"
editions["MIR"] = "Mirage"
editions["VIS"] = "Visions"
editions["5ED"] = "Fifth Edition"
editions["POR"] = "Portal"
editions["WTH"] = "Weatherlight"
editions["TMP"] = "Tempest"
editions["STH"] = "Stronghold"
editions["EXO"] = "Exodus"
editions["UGL"] = "Unglued"
editions["USG"] = "Urzas Saga"
editions["ATH"] = "Anthologies"
editions["ULG"] = "Urzas Legacy"
editions["6ED"] = "Sixth Edition"
editions["UDS"] = "Urzas Destiny"

all_cards = []

# Open test file
with open('testing.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=";", )
    first_done = False
    for row in reader:
        if first_done:
            all_cards.append({ "name": row[0], "original_name": row[1], "language": row[2], "edition": row[3] })
        first_done = True

for card in all_cards:
    print("Gathering '%s'/'%s' from '%s'..." % (card['name'], card["original_name"], editions[card['edition']]))

    # Build URL
    fixed_name = urllib.quote_plus(card['name'])
    fixed_edition = urllib.quote_plus(editions[card['edition']])
    url = "https://www.cardmarket.com/de/Magic/Products/Singles/%s/%s" % (fixed_edition, fixed_name)
    r = requests.get(url)

    if r.status_code == 200:
        d = pq(r.text)

        outer = d('#tabContent-info').find('.info-list-container').find('dl')

        labels = outer.find('dt')
        values = outer.find('dd')

        offset = 0
        for label in labels:
            if pq(label).text().strip() == "ab":
                card['price'] = pq(values.eq(offset)).text()
                continue
            offset = offset+1
            


        card['rarity'] = pq(values.eq(0).find("span").eq(0)).attr('data-original-title')


print "*"*80
for card in all_cards:
    print "Name:\t\t\t%s" % card['name']
    print "Englischer Name:\t%s" % card['original_name']
    print "Edition:\t\t%s" % editions[card['edition']]
    print "Preis:\t\t\t%s" % card['price'] 
    print "-"*40
