# -*- encoding: utf-8 -*-
import spoiler_parser as sp

cards = sp.parse_cards('dgm_spoiler.htm')

#sp.download_images('dgm_wizards.htm')
drops = {}
for card in cards:
    color = card.color
    if color not in drops:
        drops[color] = {}
    cmc = card.converted_mana_cost
    if card.rarity == u'C' and u'Creature' in card.card_type:
        drops[color][cmc] = drops[color].get(cmc, '') + '*'

for color, d in drops.items():
    print color
    for cmc, amount in d.items():
        print cmc, amount
