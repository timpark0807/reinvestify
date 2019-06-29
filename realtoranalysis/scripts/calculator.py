import numpy


class Calculations:

    def __init__(self, price, downpayment, interest, term, rent, expenses,vacancy):
        self.price = float(price.replace(',',''))
        self.downpayment = float(downpayment)
        self.interest = float(interest)
        self.term = float(term)
        self.rent = float(rent)
        self.expenses = float(expenses)
        self.vacancy = float(vacancy)

    def income_statement(self, other_income):
        """ Returns a dictionary with all necessary values"""
        grossrent = self.rent
        annual_grossrent = grossrent * 12

        vacancy = self.rent * (float(self.vacancy)/100)
        annual_vacancy = vacancy * 12

        other_income = other_income
        annual_other_income = other_income * 12

        operating_income = self.operating_income()
        annual_operating_income = operating_income * 12

        operating_expenses = self.monthly_expenses()
        annual_operating_expenses = operating_expenses * 12

        noi = self.noi(operating_income)
        annual_noi = noi * 12

        loan_payment = self.mortgage_calc()
        annual_loan_payment = loan_payment * 12

        cashflow = self.cashflow(noi, loan_payment)
        annual_cashflow = cashflow * 12

        cf_dict = {'grossrent': comma_dollar(grossrent),
                   'annual_grossrent': comma_dollar(annual_grossrent),
                   'vacancy': comma_dollar(vacancy),
                   'annual_vacancy': comma_dollar(annual_vacancy),
                   'other_income': comma_dollar(other_income),
                   'annual_other_income': comma_dollar(annual_other_income),
                   'operating_income': comma_dollar(operating_income),
                   'annual_operating_income': comma_dollar(annual_operating_income),
                   'operating_expenses': comma_dollar(operating_expenses),
                   'annual_operating_expenses': comma_dollar(annual_operating_expenses),
                   'noi': comma_dollar(noi),
                   'annual_noi': comma_dollar(annual_noi),
                   'loan_payment': comma_dollar(loan_payment),
                   'annual_loan_payment': comma_dollar(annual_loan_payment),
                   'cashflow': comma_dollar(cashflow),
                   'annual_cashflow': comma_dollar(annual_cashflow)}

        return cf_dict

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

        return round(mortgage_payment,2)

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
        if output < 0:
            return "(" + str(round((output * 100))*-1, 1) + '%)'
        else:
            return str(round(output*100,1)) + '%'


    def outofpocket(self, closing):
        # turn downpayment and closing into percents
        down_percent = self.downpayment/100
        closing_percent = float(closing)/100

        oop = (self.price*down_percent) + (self.price*closing_percent)
        return oop

    def cashoncash(self, cashflow, outofpocket):
        coc = ((cashflow * 12) / outofpocket) * 100
        if coc < 0:
            return "(" + str(round(coc*-1, 1)) + "%)"
        else:
            return str(round(coc,1)) + "%"


    def year30model(self, appreciation, income_growth):
        appreciation = int(appreciation)

        # set the initial value of the house, rent, and expenses for Year 0 of the model
        initial_value = self.price
        initial_rent = self.rent
        initial_expense = self.rent * .5

        # These are the form inputs for expected annual increase in house value
        appreciation_assumption = 1 + (appreciation/100)

        # calculate the monthly mortgage and down payment by calling previously defined function
        monthly_mortgage = self.mortgage_calc()
        downpayment = self.downpayment_calc()

        # Set up Loan Balance - Present Value calculation variables
        rate = (self.interest/100)/12
        num_of_periods = (self.term * 12)

        # Appreciated value used in the for loop. Year 0 values will be equal to the initial house and rent value
        appreciated_value = initial_value

        # empty lists to append loop results to
        year_list = []
        new_values_list = []
        loan_balance_list = []
        equity_list = []

        for i in range(1,31):

            # the appreciated value of the house is the initial value times appreciation assumption
            appreciated_value = round(appreciated_value * appreciation_assumption)

            loan_balance = round(numpy.pv(rate, num_of_periods - (12 * i), monthly_mortgage)) * -1

            equity = (initial_value - loan_balance + (appreciated_value-initial_value))

            year_list.append(i)
            new_values_list.append(appreciated_value)
            loan_balance_list.append(loan_balance)
            equity_list.append(equity)

            # loan_balance = round(numpy.pv((.05 / 12), 360 - (12 * i), monthly_mortgage)) * -1
        return year_list, new_values_list, loan_balance_list, equity_list




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
