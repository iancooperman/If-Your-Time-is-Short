import sys
import unittest

sys.path.append(__file__ + "/../..")
from ReutersArticleHandler import ReutersArticleHandler


class TestValidURL(unittest.TestCase):

    def test_world_us_path(self):
        self.assertTrue(ReutersArticleHandler._valid_url("https://www.reuters.com/world/us/seven-dead-shooting-half-moon-bay-calif-cbs-news-2023-01-24/"))

    def test_world_general_path(self):
        self.assertTrue(ReutersArticleHandler._valid_url("https://www.reuters.com/world/europe/tens-thousands-teachers-march-lisbon-demand-better-pay-conditions-2023-01-28/"))

    def test_world_path_must_be_article(self):
        self.assertFalse(ReutersArticleHandler._valid_url("https://www.reuters.com/world/europe/"))

    def test_business_path(self):
        self.assertTrue(ReutersArticleHandler._valid_url("https://www.reuters.com/business/energy/petrobras-geologist-who-led-pre-salt-discovery-head-division-sources-2023-01-27/"))

    def test_account_path_not_valid(self):
        self.assertFalse(ReutersArticleHandler._valid_url("https://www.reuters.com/account/register/sign-up/"))


class TestGetTitle(unittest.TestCase):

    def test_get_title(self):
        article_handler = ReutersArticleHandler(r"https://www.reuters.com/business/energy/petrobras-geologist-who-led-pre-salt-discovery-head-division-sources-2023-01-27/")

        article_title = article_handler.get_title()

        self.assertEqual(article_title, r"Petrobras 'pre-salt' geologist Carminatti to head exploration, production division")

class TestGetBody(unittest.TestCase):

    def test_get_body(self):
        article_handler = ReutersArticleHandler(r"https://www.reuters.com/business/energy/petrobras-geologist-who-led-pre-salt-discovery-head-division-sources-2023-01-27/")

        article_title = article_handler.get_body()

        self.assertEqual(article_title, r"HOUSTON, Jan 27 (Reuters) - The new Chief Executive of Brazil's Petrobras, Jean Paul Prates, has picked geologist Mario Carminatti to head the oil company's exploration and production division, people with knowledge of the information said on Friday. As the company's chief geologist, Carminatti is highly respected at Petrobras for having led the discovery in 2006 of one of the world's largest offshore oil deposits this century, known as 'the pre-salt' - oil reservoirs tapped under a thick layer of salt beneath the Atlantic seabed. The board of directors of Petrobras, formally known as Petroleo Brasileiro SA , has yet to formally approve the composition of the new executive team, the people said, declining to be identified because the information was private. The people said the group includes Prates' business partner Sergio Caetano Leite as chief financial officer, Mauricio Tolmasquim as chief energy transition officer and William Franca as head of refining. Petrobras said in a securities filing it had not received official statements regarding the nomination of any executive. It added the nominees would need to go through the firm's internal governance procedures. Prates sealed Carminatti's choice in a meeting on Thursday at the Presidential Palace with President Luiz Inacio Lula da Silva, Chief of Staff Rui Costa and Workers Party leader Gleisi Hoffmann, one of the people said. Carminatti was not present. Carminatti has preferred to keep a low profile at Petrobras in the past, previous CEOs having failed to convince him to take a post as head of a division. He won praise for the pre-salt discovery, pressing on with drilling though the salt barrier that alone was deeper than any well that Petrobras, the world's leader in deep-water exploration, had drilled before. It was about 2,000 meters (6,5612 feet) deep, compared with the company's previous deepest well of 1,886 meters below water. The multi-year geological program led to the largest crude discovery in that decade, in an offshore area that international oil producers had fruitlessly explored and then returned to Brazil's oil regulator. In 2008, the discovery was determined to have potential to hold more than 40 billion barrels of oil and gas, changing Lula's second presidential term. The pre-salt area is now responsible for more than 70% of Brazil's daily production of near 4 million barrels of oil and gas. Carminatti is currently involved in an almost $3 billion exploration effort in a new frontier North of Brazil, the Equatorial Margin. Petrobras experts have compared the oil deposits in the region those of nearby Guyana.")

if __name__ == '__main__':
    unittest.main()