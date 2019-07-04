import unittest
from realtoranalysis.scripts.refactor_calculator import Calculate


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.property = Calculate('100000', '20', '5.0', '30', '1500', '50', '10', '2')

    def test_down_payment(self):
        # test that 20% down of 100k is equal to 20k
        self.assertEqual(self.property.down_payment(), 20000)

    def test_outofpocket(self):
        # test that 20% down and 2% closing cost on 100k price is 22k out of pocket
        self.assertEqual(self.property.outofpocket(), 22000)

    def test_mortgage_payment(self):
        self.assertEqual(self.property.mortgage_payment(), 429)

    def test_vacancy_loss(self):
        # test vacancy loss on a 1500 rent at 10%
        self.assertEqual(self.property.vacancy_loss(), 150)

    def test_operating_income(self):
        # operating_income = rent - vacancy_loss
        self.assertEqual(self.property.operating_income(), 1350)

    def test_operating_expense(self):
        # tests operating expenses with rate of 50%
        self.assertEqual(self.property.operating_expense(), 750)

    def test_noi(self):
        # noi = operating_income - operating_expense
        self.assertEqual(self.property.noi(), 600)

    def test_cashflow(self):
        # cash flow = noi - mortgage
        self.assertEqual(self.property.cashflow(), 171)

    def test_cap_rate(self):
        self.assertEqual(self.property.cap_rate(), '7.2%')

    def test_coc(self):
        self.assertEqual(self.property.cashoncash(), '9.3%')


if __name__ == '__main__':
    unittest.main()
