import unittest
from realtoranalysis.scripts.calculator import Calculations


class TestScraper(unittest.TestCase):

    def setUp(self):
        self.house = Calculations('100000', '20', '5.0', '30', '1500', '50', '10')


    def test_downpayment_calc(self):

        # test that 20% down of 100k is equal to 20k

        self.assertEqual(self.house.downpayment_calc(), 20000)


    def test_mortgage_calc(self):
        self.assertEqual(self.house.mortgage_calc(), 429)


    def test_operating_income(self):
        # tests operating income with a 10% vacancy loss

        self.assertEqual(self.house.operating_income(10), 1350)


    def test_noi(self):
        # tests net operating income using operating income at a 10% vacancy
        oi = self.house.operating_income(10)
        self.assertEqual(self.house.noi(oi), 600)


    def test_cashflow(self):
        oi = self.house.operating_income(10)
        net_operating_income = self.house.noi(oi)
        mortgage = self.house.mortgage_calc()
        self.assertEqual(self.house.cashflow(net_operating_income, mortgage), 171)


    def test_outofpocket(self):
        self.assertEqual(self.house.outofpocket(3), 23000)

if __name__ == '__main__':
    unittest.main()
