# -*- coding: utf-8 -*-
import csv
import requests
import urllib
from pyquery import PyQuery as pq
import pprint

import json


def read_editions_from_file(file):
    with open(file, "r") as read_file:
        data = read_file.read()
    return data

def parse_editions(json_str):
    if json_str is None:
        return {}
    
    return json.loads(json_str)

editions = parse_editions(read_editions_from_file("./editions.json"))

all_cards = []

def gather_cardmarket(card):
    mkm_data = {}
    mkm_name = editions[card['edition']]['mapping']['cardmarket']

    # Build URL
    fixed_name = urllib.quote_plus(card['name'])
    fixed_edition = urllib.quote_plus(mkm_name)
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
                mkm_data['price'] = pq(values.eq(offset)).text()
                continue
            offset = offset+1

        mkm_data['rarity'] = pq(values.eq(0).find("span").eq(0)).attr('data-original-title')
    
    card['mkm'] = mkm_data
    return card
    


# Open test file
with open('testing.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=";", )
    first_done = False
    for row in reader:
        if first_done:
            all_cards.append({ "name": row[0], "original_name": row[1], "language": row[2], "edition": row[3] })
        first_done = True

for card in all_cards:

    edition_name = editions[card['edition']]['name']
    

    print("Card: '%s'/'%s' from '%s'..." % (card['name'], card["original_name"], edition_name))

    print("  -> Checking cardmarket...")
    card = gather_cardmarket(card)


print "*"*80

for card in all_cards:
    print "Name:\t\t\t%s" % card['name']
    print "Englischer Name:\t%s" % card['original_name']
    print "Edition:\t\t%s" % editions[card['edition']]['name']
    print "Preis [MKM]:\t\t%s" % card['mkm']['price'] 
    print "-"*40

print "*"*80
pprint.pprint(all_cards)
