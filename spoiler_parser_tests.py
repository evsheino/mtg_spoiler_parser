# -*- encoding: utf-8 -*-
import spoiler_parser as sp
from bs4 import BeautifulSoup
import unittest

class TestParser(unittest.TestCase):

    def setUp(self):
        mighty_leap_elem = """
<div class="spoiler-card-text">
                                       
<div class="t-spoiler card-color-White card-type-Instant"  id="Mighty Leap">
    <div class="t-spoiler-container">
        <header class="t-spoiler-header common">
            
                <h2><a class="j-search-html" href="http://www.mtgsalvation.com/cards/modern-masters-2015-edition/25138-mighty-leap">Mighty Leap</a></h2>
            
            <ul class="t-spoiler-mana">
                
                    <span class="mana-icon mana-colorless-01 tip" title="1 Colorless Mana">1</span>
                
                    <span class="mana-icon mana-white tip" title="1 White Mana">W</span>
                
            </ul>
        </header>
        <section class="t-spoiler-content">
            <div class="t-spoiler-meta">
                <span class="t-spoiler-type j-search-html">Instant</span>
                <span class="t-spoiler-rarity"><span class="mtg-set-icon mtg-set-modern-masters-2015-edition-common" style="background: url('http://media-dominaria.cursecdn.com/avatars/thumbnails/66/14/22/14/MM2.png') width: 22px; height: 14px;"></span></span>
            </div>
            
            <div class="t-spoiler-ability">
                
                <p>Target creature gets +2/+2 and gains flying until end of turn.</p>
                
                <input class="j-search-val" type="hidden" value="Target creature gets +2/+2 and gains flying until end of turn." />
            </div>
            
            <div class="t-spoiler-flavor">
                <p>&quot;The southern fortress taken by invaders? Heh, sure.... when elephants fly.&quot;
-Brezard Skeinbow, captain of the guard.</p>
            </div>
            
            <div class="t-spoiler-edition">
                <span class="t-spoiler-artist"><p>illus. RK Post # 24/249</p></span>
            </div>
        </section>
        <footer class="t-spoiler-footer">
            <p>
                
                    <span class="tip" title="Mothership">SRC</span>
                
                    <a href="http://www.mtgsalvation.com/cards?filter-search=Mighty Leap" class="tip" title="This card is a reprint">RP</a>
                
            </p>
            
        </footer>
    </div>
</div>

</div>
        """

        water_servant_elem = """
<div class="spoiler-card-text">
                                       
<div class="t-spoiler card-color-Blue card-type-Creature"  id="Water Servant">
    <div class="t-spoiler-container">
        <header class="t-spoiler-header uncommon">
            
                <h2><a class="j-search-html" href="http://www.mtgsalvation.com/cards/modern-masters-2015-edition/25238-water-servant">Water Servant</a></h2>
            
            <ul class="t-spoiler-mana">
                
                    <span class="mana-icon mana-colorless-02 tip" title="2 Colorless Mana">2</span>
                
                    <span class="mana-icon mana-blue tip" title="1 Blue Mana">U</span>
                
                    <span class="mana-icon mana-blue tip" title="1 Blue Mana">U</span>
                
            </ul>
        </header>
        <section class="t-spoiler-content">
            <div class="t-spoiler-meta">
                <span class="t-spoiler-type j-search-html">Creature - Elemental</span>
                <span class="t-spoiler-rarity"><span class="mtg-set-icon mtg-set-modern-masters-2015-edition-uncommon" style="background: url('http://media-dominaria.cursecdn.com/avatars/thumbnails/66/15/22/14/MM2.png') width: 22px; height: 14px;"></span></span>
            </div>
            
            <div class="t-spoiler-ability">
                
                <p><span class="tip mana-icon mana-blue" title="1 Blue Mana">U</span>: Water Servant gets +1/-1 until end of turn.
</p>
                
                <p></p>
                
                <p><span class="tip mana-icon mana-blue" title="1 Blue Mana">U</span>: Water Servant gets -1/+1 until end of turn.</p>
                
                <input class="j-search-val" type="hidden" value="{U}: Water Servant gets +1/-1 until end of turn.

{U}: Water Servant gets -1/+1 until end of turn." />
            </div>
            
            <div class="t-spoiler-flavor">
                <p>&quot;This creature has innate perceptiveness. It knows when to rise and when to vanish into the tides.&quot;—Jestus Dreya, Of Elements and Eternity</p>
            </div>
            
            <div class="t-spoiler-edition">
                <span class="t-spoiler-artist"><p>illus. Igor Kieryluk # 69/249</p></span>
            </div>
        </section>
        <footer class="t-spoiler-footer">
            <p>
                
                    <a href="http://www.mtgsalvation.com/cards?filter-search=Water Servant" class="tip" title="This card is a reprint">RP</a>
                
            </p>
            
                    <span class="t-spoiler-stat">3/4</span>
                
        </footer>
    </div>
</div>

                                </div>
        """

        self.mighty_leap = BeautifulSoup(mighty_leap_elem)

        self.water_servant = BeautifulSoup(water_servant_elem)

    def test_parse_name(self):
        name = sp.parse_name(self.mighty_leap)
        self.assertEqual(name, u"Mighty Leap")

    def test_parse_rarity(self):
        rarity = sp.parse_rarity(self.mighty_leap)
        self.assertEqual(rarity, u"C")

    def test_parse_type(self):
        card_type = sp.parse_type(self.mighty_leap)
        self.assertEqual(card_type, u"Instant")

    def test_parse_mana_cost(self):
        mana_cost = sp.parse_mana_cost(self.mighty_leap)
        self.assertEqual(mana_cost, [u"1", u"W"])

    def test_parse_symbol(self):
        symbol = sp.parse_symbol(u"W")
        self.assertEqual(symbol, u"W")

        symbol = sp.parse_symbol(u"(R/W)")
        self.assertEqual(symbol, u"(R/W)")

        symbol = sp.parse_symbol(u"(R/P)")
        self.assertEqual(symbol, u"{!R}")

    def test_parse_color(self):
        color = sp.parse_color([u"3", u"W"])
        self.assertEqual(color, u"W")

        color = sp.parse_color([u"(R/W)", u"(R/W)", u"(R/W)"])
        self.assertEqual(color, u"RW")

        color = sp.parse_color([u"X", u"(R/W)"])
        self.assertEqual(color, u"RW")

    def test_strip_symbol(self):
        colors = sp.strip_symbol("(R/W)")
        self.assertEqual(colors, [u"R", u"W"])
        
        colors = sp.strip_symbol(u"X")
        self.assertEqual(colors, [])

    def test_parse_converted_cost(self):
        cost = sp.parse_converted_cost([u"X", u"X", u"(R/W)"])
        self.assertEqual(cost, 1)

    def test_parse_power_and_toughness(self):
        pt = sp.parse_power_and_toughness(self.water_servant)
        self.assertEqual(pt, [u"3", u"4"])

    def test_parse_text(self):
        self.maxDiff = None
        text = sp.parse_text(self.mighty_leap)
        self.assertEqual(text, u"Target creature gets +2/+2 and gains flying until end of turn.")

        text = sp.parse_text(self.water_servant)
        real_text = u"{U}: Water Servant gets +1/-1 until end of turn. {U}: Water Servant gets -1/+1 until end of turn."
        self.assertEqual(text, real_text)

if __name__ == "__main__":
    unittest.main()
