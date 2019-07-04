import unittest
from realtoranalysis.scrape import listing_json
from realtoranalysis.oldscrape import listing_meta


class TestScraper(unittest.TestCase):

    def test_listing_json(self):

        url = 'https://www.realtor.com/realestateandhomes-detail/104-Aruba-Ct_Austin_TX_78734_M75037-62575?view=qv'
        self.assertEqual(listing_meta(url), ('799000', '4', '3.5', '4012'))

if __name__ == '__main__':
    unittest.main()