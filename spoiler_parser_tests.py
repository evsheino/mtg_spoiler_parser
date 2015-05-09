# -*- encoding: utf-8 -*-
import spoiler_parser as sp
from bs4 import BeautifulSoup
import unittest

class TestParser(unittest.TestCase):

    def setUp(self):
        assault_griffin_table = """
            <table border="0" cellspacing="0" cellpadding="5" width="290" align="center" style="border: 1px solid black;background-color:white;color: black;">
                <tr style="background-color: #ffffcc;border-bottom: 1px solid #aaa;">
                    <td width="220px">
                        <a name="6787"></a>
                        <a name="Assault Griffin"></a>
                        <h3 style="margin: 0;">*Assault Griffin</h3>
                    </td>
                    <td align="right" width="80px">
                        <img src="http://forums.mtgsalvation.com/images/smilies/mana3.gif" alt="3" class="inlineimg" style="border: none;" />
                        <img src="http://forums.mtgsalvation.com/images/smilies/manaw.gif" alt="w" class="inlineimg" style="border: none;" />
                    </td>
                </tr>
                <tr style="border-bottom: 1px dotted #aaa;">
                    <td width="220px">
                        Creature - Griffin
                    </td>
                    <td align="right" width="80px">
                        <img src="http://mtgsalvation.com/images/spoiler/gatecrash-common.gif" alt="Common" />
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        Flying
                    </td>
                </tr><tr><td colspan="3"><i>"The Simic offer a prize to any biomancer who can breed a krasis to match a griffin in the air. It's never been claimed."<br />
            Libuse, Boros sergeant</i></td></tr>
                <tr style="border-top: 1px dotted #aaa;">
                    <td>
                        Illus. Eric Velhagen <i>#4/249</i>
                    </td>
                    <td align="right">
                        3/2
                    </td>
                </tr>
            </table>
        """

        simic_fluxmage_table = """
            <table border="0" cellspacing="0" cellpadding="5" width="290" align="center" style="border: 1px solid black;background-color:white;color: black;">
		    <tr style="background-color: #99ccff;border-bottom: 1px solid #aaa;">
		        <td width="220px">
		            <a name="6652"></a>
		            <a name="Simic Fluxmage"></a>
		            <h3 style="margin: 0;">
                        <a href="http://forums.mtgsalvation.com/attachment.php?attachmentid=138020&d=1356148776" style="color: #3E5E7B;">Simic Fluxmage <img src="http://mtgsalvation.com/images/image.png" />
                        </a>
                    </h3>
		        </td>
		        <td align="right" width="80px">
                    <img src="http://forums.mtgsalvation.com/images/smilies/mana2.gif" alt="2" class="inlineimg" style="border: none;" />
                    <img src="http://forums.mtgsalvation.com/images/smilies/manau.gif" alt="u" class="inlineimg" style="border: none;" />
                </td>
		    </tr>
		    <tr style="border-bottom: 1px dotted #aaa;">
		        <td width="220px">Creature - Merfolk Wizard</td>
		        <td align="right" width="80px"><img src="http://mtgsalvation.com/images/spoiler/gatecrash-uncommon.gif" alt="Uncommon" /></td>
		    </tr>
		    <tr>
		        <td colspan="2">
                    Evolve <i><i>(Whenever a creature enters the battlefield under your control, if that creature has greater power or toughness than this creature, put a +1/+1 counter on this creature.)</i></i><br />
                    <img src="http://forums.mtgsalvation.com/images/smilies/mana1.gif" alt="1" /><img src="http://forums.mtgsalvation.com/images/smilies/manau.gif" alt="{U}" />
                    , <img src="http://forums.mtgsalvation.com/images/smilies/tap.gif" alt="{T}" />: Move a +1/+1 counter from Simic Fluxmage onto target creature.
                </td>
            </tr>
            <tr style="border-top: 1px dotted #aaa;">
                <td>Illus. Karl Kopinski <i>#49/249</i></td>
                <td align="right">1/2</td>
            </tr>
        </table>
        """

        armed_dangerous_table = """
            <table border="0" cellspacing="0" cellpadding="5" width="290" align="center" style="border: 1px solid black;background-color:white;color: black;">
                        <tr style="background: url(http://mtgsalvation.com/images/spoiler/bg/.gif) 50% 50%;border-bottom: 1px solid #aaa;">
                            <td width="220px">
                                <a name="6946"></a>
                                <a name="Armed // Dangerous"></a>
                                <h3 style="margin: 0;"><a href="http://forums.mtgsalvation.com/attachment.php?attachmentid=141190&d=1365601141" style="color: #3E5E7B;">Armed // Dangerous <img src="http://mtgsalvation.com/images/image.png" /></a></h3>
                            </td>
                            <td align="right" width="80px"><img src="http://forums.mtgsalvation.com/images/smilies/mana1.gif" alt="1" class="inlineimg" style="border: none;" /><img src="http://forums.mtgsalvation.com/images/smilies/manar.gif" alt="r" class="inlineimg" style="border: none;" />//<img src="http://forums.mtgsalvation.com/images/smilies/mana3.gif" alt="3" class="inlineimg" style="border: none;" /><img src="http://forums.mtgsalvation.com/images/smilies/manag.gif" alt="g" class="inlineimg" style="border: none;" /></td>
                        </tr>
                        <tr style="border-bottom: 1px dotted #aaa;">
                            <td width="220px">Sorcery // Sorcery</td>
                            <td align="right" width="80px"><img src="http://mtgsalvation.com/images/spoiler/dragons-maze-uncommon.gif" alt="Uncommon" /></td>
                        </tr>
                        <tr>
                            <td colspan="2">Target creature gets +1/+1 and gains double strike until end of turn.<br />
            //<br />
            All creatures able to block target creature do so this turn.<br />
            Fuse <i>(You may cast one or both halves of this card from your hand.)</i></td></tr><tr style="border-top: 1px dotted #aaa;"><td>Illus. David Palumbo <i>#122/166</i></td><td align="right"></td></tr></table>
        """

        soup = BeautifulSoup(assault_griffin_table)
        self.a = soup.table.find_all('a')[1]

        soup = BeautifulSoup(simic_fluxmage_table)
        self.fluxmage_a = soup.table.find_all('a')[1]

        soup = BeautifulSoup(armed_dangerous_table)
        self.armed_dangerous_a = soup.table.find_all('a')[1]

    def test_parse_name(self):
        name = sp.parse_name(self.a)
        self.assertEqual(name, u"Assault Griffin")

    def test_parse_rarity(self):
        rarity = sp.parse_rarity(self.a)
        self.assertEqual(rarity, u"C")

    def test_parse_type(self):
        card_type = sp.parse_type(self.a)
        self.assertEqual(card_type, u"Creature - Griffin")

    def test_parse_mana_cost(self):
        mana_cost = sp.parse_mana_cost(self.a)
        self.assertEqual(mana_cost, [u"3", u"W"])

    def test_parse_symbol(self):
        symbol = sp.parse_symbol(u"W")
        self.assertEqual(symbol, u"W")

        symbol = sp.parse_symbol(u"rw")
        self.assertEqual(symbol, u"(R/W)")

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

    def test_parse_mana_cost(self):
        mana_cost = sp.parse_mana_cost(self.a)
        self.assertEqual(mana_cost, [u"3", u"W"])

    def test_parse_converted_cost(self):
        cost = sp.parse_converted_cost([u"X", u"X", u"(R/W)"])
        self.assertEqual(cost, 1)

    def test_parse_power_and_toughness(self):
        pt = sp.parse_power_and_toughness(self.a)
        self.assertEqual(pt, [u"3", u"2"])

    def test_parse_text(self):
        self.maxDiff = None
        text = sp.parse_text(self.a)
        self.assertEqual(text, u"Flying")

        text = sp.parse_text(self.fluxmage_a)
        real_text = u"Evolve (Whenever a creature enters the battlefield under your control, if that creature has greater power or toughness than this creature, put a +1/+1 counter on this creature.)  1{U}, {T}: Move a +1/+1 counter from Simic Fluxmage onto target creature."
        self.assertEqual(text, real_text)

    def _test_new_parse_text(self):
        td = """
            <td colspan="2">
                Evolve <i><i>(Whenever a creature enters the battlefield under your control, if that creature has greater power or toughness than this creature, put a +1/+1 counter on this creature.)</i></i><br />
                <img src="http://forums.mtgsalvation.com/images/smilies/mana1.gif" alt="1" />
                <img src="http://forums.mtgsalvation.com/images/smilies/manau.gif" alt="{U}" />
                , <img src="http://forums.mtgsalvation.com/images/smilies/tap.gif" alt="{T}" />: Move a +1/+1 counter from Simic Fluxmage onto target creature.
            </td>
        """
        td = """
		        <td colspan="2">Flying<br />
Extort <i>(Whenever you cast a spell, you pay <img
src="http://forums.mtgsalvation.com/images/smilies/manaWB.gif" alt="{WB}" />. If
you do, each opponent loses 1 life and you gain that much life.)</i></td>
"""
        soup = BeautifulSoup(td)
        text = parse_text(soup.td)

    def test_parse_split_card_mana_cost(self):
        mana_cost = sp.parse_mana_cost(self.armed_dangerous_a)
        self.assertEqual(mana_cost, [u'1', u'R', u'//', u'3', u'G'])

if __name__ == "__main__":
    unittest.main()
