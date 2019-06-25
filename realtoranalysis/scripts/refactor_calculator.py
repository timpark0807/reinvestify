import numpy


class Calculations:

    def __init__(self, price, downpayment, interest, term, rent, expense, vacancy, closing):
        self.price = float(price.replace(',',''))
        self.downpayment = float(downpayment)/100     # convert downpayment to percent
        self.interest = float(interest)/100         # convert interest to percent
        self.term = float(term)
        self.rent = float(rent)
        self.expense = float(expense)/100
        self.vacancy = float(vacancy)/100
        self.closing = float(closing)/100

    def down_payment(self):

        # The down payment amount is the purchase price x percent down
        result = self.price * self.downpayment

        return result


    def mortgage_payment(self):
        """ Calculates the monthly mortgage payment """

        # Annual Rate divided by number of payments per
        p_int = self.interest/12

        # n = how many months mortgage will be amortized over
        n = 12 * int(self.term)

        # calculating discount factor
        d = ((1+p_int)**n)-1
        d2 = (1.0+p_int)**n
        d3 = p_int * d2
        discountfactor = d/d3

        # 20% downpayment means we are taking out a loan for 80% of the price
        loan_amount = (1-self.downpayment) * self.price

        # monthly payment
        mortgage_payment = loan_amount/discountfactor

        return mortgage_payment

    def outofpocket(self):

        out_of_pocket = (self.price * self.downpayment) + (self.price * self.closing)
        return out_of_pocket

    def vacancy_loss(self):
        vacancy_loss = self.rent * self.vacancy
        return vacancy_loss

    def operating_income(self):

        # operating income is gross rent minus how much we project to lose
        operating_income = (self.rent) - self.vacancy_loss()

        return operating_income

    def operating_expense(self):

        # projecting expenses as as percent of the monthly income
        operating_expense = (self.rent) * (self.expense)
        return operating_expense

    def noi(self):

        # net operating income is equal to income minus expenses
        noi = self.operating_income() - self.operating_expense()

        return noi

    def cashflow(self):
        return self.noi() - self.mortgage_payment()

    def cap_rate(self):

        cap_rate = (self.noi() * 12) / self.price
        if cap_rate < 0:
            return "(" + str(round((cap_rate * 100))*-1, 1) + '%)'
        else:
            return str(round(cap_rate * 100, 1)) + '%'

    def cashoncash(self):
        coc = ((self.cashflow() * 12) / self.outofpocket()) * 100
        if coc < 0:
            return "(" + str(round(abs(coc), 1)) + "%)"
        else:
            return str(round(coc, 1)) + "%"


property = Calculations('100,000', '20', '5.0', '30', '1500', '50', '10','2')
print('downpayment:', property.down_payment())
print('mortgage payment:', property.mortgage_payment())
print('out of pocket', property.outofpocket())
print('vacancy loss:', property.vacancy_loss())
print('operating income:', property.operating_income())
print('operating_expense:', property.operating_expense())
print('noi:', property.noi())
print('cashflow:', property.cashflow())
print('caprate:', property.cap_rate())
print('cash on cash:', property.cashoncash())

def comma_dollar(number):
    number = int(number)
    if number < 0:
        payment_1 = format(round(number * -1), ',d')
        str_payment = "($" + str(payment_1) + ")"
        return str_payment
    else:
        payment_1 = format(round(number), ',d')
        str_payment = "$" + str(payment_1)
        return str_payment
