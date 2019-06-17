
class Calculations:

    def __init__(self, price, downpayment, interest, term, rent, expenses,vacancy):
        self.price = float(price)
        self.downpayment = float(downpayment)
        self.interest = float(interest)
        self.term = float(term)
        self.rent = float(rent)
        self.expenses = float(expenses)
        self.vacancy = float(vacancy)



    def downpayment_calc(self):

        # turn down payment into a percentage
        down_percent = self.downpayment/100
        down_payment = self.price * down_percent

        return round(down_payment)

    def mortgage_calc(self):
        """ Calculates the monthly mortgage payment from inputs above """

        #  Turn form inputs into percentages
        interest_percent = self.interest/100
        down_percent = self.downpayment/100

        # Annual Rate divided by number of payments per
        p_int = interest_percent/12

        # n = how many months mortgage will be amortized over
        n = 12 * int(self.term)

        # calculating discount factor
        d = ((1+p_int)**n)-1
        d2 = (1.0+p_int)**n
        d3 = p_int * d2
        discountfactor = d/d3

        # 20% downpayment means we are taking out a loan for 80% of the price
        loan_amount = (1-down_percent) * self.price

        # monthly payment
        mortgage_payment = loan_amount/discountfactor

        return round(mortgage_payment)

    def operating_income(self):
        # vacancy in terms of percent
        vacancy_percent = float(self.vacancy)/100

        # we project to lose this much of rent due to vacancy
        vacancy_loss = self.rent * vacancy_percent

        # operating income is gross rent minus how much we project to lose
        operating_income = self.rent - vacancy_loss

        return round(operating_income)

    def monthly_expenses(self):
        # expenses are entered on the form as a whole number, convert it to a percent here
        expenses_percent = self.expenses / 100

        # projecting expenses as as percent of the monthly income
        monthly_expenses = (self.rent) * (expenses_percent)
        return monthly_expenses

    def noi(self, oi):
        # expenses are entered on the form as a whole number, convert it to a percent here
        expenses_percent = self.expenses/100

        # projecting expenses as as percent of the monthly income
        monthly_expenses = (self.rent)*(expenses_percent)

        # net operating income is equal to income minus expenses
        noi = oi - monthly_expenses

        return round(noi)

    def cashflow(self, noi, mortgage):
        return round(noi - mortgage)


    def cap_rate(self):
        # vacancy in terms of percent
        vacancy_percent = float(self.vacancy)/100

        # we project to lose this much of rent due to vacancy
        vacancy_loss = self.rent * vacancy_percent

        # operating income is gross rent minus how much we project to lose
        operating_income = (self.rent - vacancy_loss) * 12

        noi = operating_income * (self.expenses/100)
        output = (noi/self.price)
        return str(output*100) + '%'


    def outofpocket(self, closing):
        # turn downpayment and closing into percents
        down_percent = self.downpayment/100
        closing_percent = float(closing)/100

        oop = (self.price*down_percent) + (self.price*closing_percent)
        return oop


def comma_dollar(number):
    payment_1 = format(round(number), ',d')
    str_payment = "$" + str(payment_1)
    return str_payment
