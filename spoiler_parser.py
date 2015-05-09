# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
import os.path
import codecs
import re
import sys

class MtgCard(object):
    """
    An MtG card.
    """

    def __init__(self, a, mtg_set):
        """
        @param a: the a element in the spoiler source as a BeautifulSoup element.
        @param mtg_set: the set of the card.
        """

        self.mtg_set = mtg_set
        self.name = parse_name(a).replace(u'’', u'').replace(u',', u'').replace(u"'", '')
        self.rarity = parse_rarity(a)
        self.card_type = parse_type(a)
        mana_cost = parse_mana_cost(a)
        self.mana_cost = u''.join(mana_cost)
        self.converted_mana_cost = parse_converted_cost(mana_cost)
        self.color = parse_color(mana_cost)
        self.text = parse_text(a)

        power_and_toughness = parse_power_and_toughness(a)
        try:
            self.power = power_and_toughness[0]
            self.toughness = power_and_toughness[1]
        except IndexError:
            # No power/toughness for this card
            self.power = u''
            self.toughness = u''

def parse_name(a):
    name = a.attrs.get('name')
    if name:
        name = unicode(name)
        if not name.isnumeric():
            return name.strip()
    raise TypeError

def parse_rarity(a):
    return a.parent.parent.next_sibling.next_sibling.find('img').attrs.get('alt') \
        .strip()[:1]

def parse_type(a):
    return a.parent.parent.next_sibling.next_sibling.td.string.strip()

def parse_symbol(symbol):
    """
    Parse the mana symbol and return it in LackeyCCG format.
    """

    s = unicode(symbol)
    if not s.isnumeric():
        if len(s) == 2:
            # Hybrid mana
            s = u'({}/{})'.format(s[0], s[1]).upper()
    return s

def parse_mana_cost(a):
    """
    Get the mana cost of a card.

    @param a: the a element of the card in the MtgSalvation spoiler.
    """

    mana_cost = []
    td = a.parent.next_sibling.next_sibling
    
    for e in td:
        try:
            symbol = parse_symbol(e.attrs.get('alt').upper())
        except AttributeError:
            if e != u'//':
                continue
            symbol = e
        mana_cost.append(symbol)
    return mana_cost

def parse_color(mana_cost):
    color = u''
    for symbol in mana_cost:
        symbol_colors = strip_symbol(symbol)
        for symbol_color in symbol_colors:
            if not symbol_color in color:
                symbol_color = unicode(symbol_color)
                color += symbol_color.upper()
    return color

def strip_symbol(symbol):
    m = re.findall('[a-wzA-WZ]', symbol)
    return m

def parse_converted_cost(mana_cost):
    skip = ['X', '//']
    cost = 0
    for symbol in mana_cost:
        symbol = unicode(symbol)
        if symbol.isnumeric():
            cost += int(symbol)
        elif symbol.upper() in skip:
            continue
        else:
            cost += 1
    return cost

def parse_power(a):
    try:
        power = self.parse_power_and_toughness()[0]
    except IndexError:
        power = u''
    return power

def parse_toughness(a):
    try:
        toughness = self.parse_power_and_toughness()[2]
    except IndexError:
        toughness = u''
    return toughness

def parse_text(a):
    tag = a.parent.parent.parent.find(colspan='2')
    return parse_elem_text(tag).strip()

def parse_elem_text(tag):
    """
    Parse the given tag recursively and return the contents stripped of all
    tags. Include image tags' alt text.
    """
    if tag.name == 'img':
        return tag.attrs.get('alt')
    text = u''
    # Try to parse the tag recursively. If it's a NavigableString, return it and end the recursion.
    try:
        for content in tag.contents:
            text += parse_elem_text(content)
        return text
    except AttributeError:
        # NavigableString encountered: return it
        return u'{} '.format(tag.strip())


def parse_power_and_toughness(a):
    """
    Parse the power and toughness.

    Return the power and toughness as a list: [power, toughness]
    """

    pt = []
    parent = a.parent.parent
    for elem in parent.next_siblings:
        try:
            for child in elem.children:
                try:
                    pt_string = child.string.strip()
                except AttributeError:
                    continue
                try:
                    int(pt_string.replace(u'/', u'').replace(u'*', u'0'))
                    pt = child.string.strip().split('/')
                except ValueError:
                    continue
        except AttributeError:
            pass
    return pt 

def write_card_list(cards, output_file):
    """
    Write a card list in the LackeyCCG format.

    @param cards: a list of MtgCard objects.
    @param output_file: the path to save the file.
    """

    output_file = codecs.open(output_file, 'w+', 'utf-8')
#    output_file.write(
#        u'Name\tSet\tImageFile\tColor\tCost\tConvertedCost\tType\tPower\tToughness\tRarity\tText\n')

    for card in cards:
        output_file.write(
            u'{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            card.name,
            card.mtg_set,
            card.name.replace(u'//', u'&'), # Image file name
            card.color,
            card.mana_cost,
            card.converted_mana_cost,
            card.card_type, 
            card.power, 
            card.toughness,
            card.rarity, 
            '', # Sound
            '', # Script
            card.text))
    output_file.close()

def parse_cards(src, set_name):
    """
    Parse the MtgSalvation spoiler for card information.

    Return a list of MtgCard objects.

    @param src: path to a locally saved copy of the MtgSalvation
                spoiler.
    """

    cards = []
    f = open(src)
    soup = BeautifulSoup(f)
    for table in soup.find_all('table'):
        try:
            a = table.find_all('a')[1]
        except IndexError:
            continue
        try:
            cards.append(MtgCard(a, set_name))
        except TypeError:
            continue
    f.close()
    return cards

if __name__ == '__main__':
    cards = parse_cards(sys.argv[1], sys.argv[2])
    write_card_list(cards, sys.argv[3])
