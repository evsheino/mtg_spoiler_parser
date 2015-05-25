# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
import os.path
import codecs
import re
import sys

# Mana formats
NORMAL_MANA = "{}"
PHYREXIAN_MANA = "{{!{}}}"
HYBRID_MANA = "({}/{})"

# Spoiler mana formats for regex matching
NORMAL_MANA_RE = r"([wWuUbBrRgG])"
SPOILER_PHYREXIAN_MANA_RE = r"\(({})/[pP]\)".format(NORMAL_MANA_RE)
SPOILER_HYBRID_MANA_RE = r"\(({})/({})\)".format(r"(\d+|[wWuUbBrRgG])", NORMAL_MANA_RE)

# Mana cost transform dict
MANA_DICT = { NORMAL_MANA_RE: NORMAL_MANA, 
        SPOILER_PHYREXIAN_MANA_RE: PHYREXIAN_MANA,
        SPOILER_HYBRID_MANA_RE: HYBRID_MANA }

class MtgCard(object):
    """
    An MtG card.
    """

    def __init__(self, elem, mtg_set):
        """
        @param elem: an element containing the information of the card 
                     in the spoiler source as a BeautifulSoup element.
        @param mtg_set: the set of the card.
        """

        self.mtg_set = mtg_set
        self.name = parse_name(elem).replace(u'’', u'').replace(u',', u'').replace(u"'", '')
        self.rarity = parse_rarity(elem)
        self.card_type = parse_type(elem)
        mana_cost = parse_mana_cost(elem)
        self.mana_cost = u''.join(mana_cost)
        self.converted_mana_cost = parse_converted_cost(mana_cost)
        self.color = parse_color(mana_cost)
        self.text = parse_text(elem)

        self.power = u''
        self.toughness = u''

        pt = parse_power_and_toughness(elem)
        if not pt is None:
            self.power = pt[0]
            try:
                self.toughness = pt[1]
            except IndexError:
                # Planeswalker
                pass

def parse_name(elem):
    return parse_elem_text(elem.find("h2"))

def parse_rarity(elem):
    return elem.find("header")["class"][1][0].upper()

def parse_type(elem):
    return elem.find("span", "t-spoiler-type").text

def parse_symbol(symbol):
    """
    Parse the mana symbol and return it in LackeyCCG format.
    """

    s = unicode(symbol)
    if s.isnumeric():
        return s

    for regex, mana_format in MANA_DICT.items():
        r = re.match(regex, s)
        if r:
            mana_symbols = r.groups()
            if len(mana_symbols) > 1:
                return unicode(mana_format.format(*mana_symbols[1:]))
            return unicode(mana_format.format(mana_symbols[0]))

    return u''

def parse_mana_cost(elem):
    """
    Get the mana cost of a card as a list.

    @param elem: the element of the card in the MtgSalvation spoiler.
    """
    mana_cost = []
    spoiler_mc = parse_elem_text(elem.find("ul", "t-spoiler-mana"), as_list=True)
    for symbol in spoiler_mc:
        mana_cost.append(parse_symbol(symbol))
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
    skip = ['X', '//', '!']
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

def parse_text(elem):
    text = elem.find("input")["value"]
    return u' '.join(re.sub(r"\[[/]*mana\]", "", text).split())

def parse_elem_text(tag, as_list=False):
    """
    Parse the given tag recursively and return the contents stripped of all
    tags.
    """
    if as_list:
        text = []
    else:
        text = u''
    # Try to parse the tag recursively. If it's a NavigableString, return it and end the recursion.
    try:
        for content in tag.contents:
            text += parse_elem_text(content, as_list)
        return text if as_list else text.strip()
    except AttributeError:
        if tag.strip() == "":
            return [] if as_list else u''
        # NavigableString encountered: return it
        if as_list:
            return [tag.strip()]
        return u'{} '.format(tag.strip())


def parse_power_and_toughness(elem):
    """
    Parse the power and toughness.

    Return the power and toughness as a list: [power, toughness]
    """

    try:
        return elem.find("span", "t-spoiler-stat").text.strip().split('/')
    except AttributeError:
        # No power/toughness
        return None

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
            card.text).replace(u"Æ", u"Ae"))
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
    for elem in soup.find_all('div', 'spoiler-card-text'):
        cards.append(MtgCard(elem, set_name))
    f.close()
    return cards

if __name__ == '__main__':
    # Params:
    # 1: Path to a locally saved copy of the MtGSalvation spoiler
    # 2: Set name
    # 3: Output file
    cards = parse_cards(sys.argv[1], sys.argv[2])
    write_card_list(cards, sys.argv[3])
