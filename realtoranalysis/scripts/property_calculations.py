import numpy


class Calculate:

    def __init__(self, price, downpayment, interest, term, rent, expense, vacancy, closing, other_income):
        self.purchase_price = float(price)
        self.downpayment = float(downpayment)/100     # convert down payment to percent
        self.interest = float(interest)/100         # convert interest to percent
        self.term = float(term)
        self.rent = float(rent)
        self.expense = float(expense)/100
        self.vacancy = float(vacancy)/100
        self.closing = float(closing)/100
        self.other_income = float(other_income)

    def get_down_payment(self):
        # The down payment amount is the purchase price x percent down
        down_payment = self.purchase_price * self.downpayment
        return round(down_payment)

    def get_discount_factor(self):
        # Annual Rate divided by number of payments per
        p_int = self.interest/12

        # n = how many months mortgage will be amortized over
        n = 12 * int(self.term)

        # calculating discount factor
        d = ((1+p_int)**n)-1
        d2 = (1.0+p_int)**n
        d3 = p_int * d2

        return d/d3

    def get_loan_amount(self):
        # 20% down payment means we are taking out a loan for 80% of the purchase price
        return (1-self.downpayment) * self.purchase_price

    def get_closing_cost(self):
        closing_cost = self.purchase_price * self.closing
        return round(closing_cost)

    def get_vacancy_loss(self):
        vacancy_loss = self.rent * self.vacancy
        return round(vacancy_loss)

    def get_operating_income(self):
        # gross rent minus how much we project to lose
        operating_income = self.rent + self.other_income - self.get_vacancy_loss()
        return round(operating_income)

    def get_operating_expense(self):
        # projecting expenses as as percent of the monthly income
        operating_expense = self.rent * self.expense
        return round(operating_expense)

    def mortgage_payment(self):
        discount_factor = self.get_discount_factor()
        loan_amount = self.get_loan_amount()
        mortgage_payment = loan_amount/discount_factor
        return round(mortgage_payment)

    def outofpocket(self):
        out_of_pocket = self.get_down_payment() + self.get_closing_cost()
        return round(out_of_pocket)

    def noi(self):
        # net operating income is equal to income minus expenses
        noi = self.get_operating_income() - self.get_operating_expense()
        return round(noi)

    def cashflow(self):
        cash_flow = self.noi() - self.mortgage_payment()
        return round(cash_flow)

    def appreciation_model(self, appreciation):
        appreciation = int(float(appreciation))

        # set the initial value of the house, rent, and expenses for Year 0 of the model
        initial_value = self.purchase_price

        # These are the form inputs for expected annual increase in house value
        appreciation_assumption = 1 + (appreciation/100)

        # calculate the monthly mortgage and down payment by calling previously defined function
        monthly_mortgage = self.mortgage_payment()
        downpayment = self.get_down_payment()

        # Set up Loan Balance - Present Value calculation variables
        rate = self.interest/12
        num_of_periods = self.term * 12

        # Appreciated value used in the for loop. Year 0 values will be equal to the initial house and rent value
        appreciated_value = initial_value

        # empty lists to append loop results to
        year_list = []
        new_values_list = []
        loan_balance_list = []
        equity_list = []

        for i in range(1, int(self.term) + 1):
            # the appreciated value of the house is the initial value times appreciation assumption
            appreciated_value = round(appreciated_value * appreciation_assumption)
            loan_balance = round(numpy.pv(rate, num_of_periods - (12 * i), monthly_mortgage)) * -1
            equity = (initial_value - loan_balance + (appreciated_value-initial_value))

            year_list.append(i)
            new_values_list.append(appreciated_value)
            loan_balance_list.append(loan_balance)
            equity_list.append(equity)

        return year_list, new_values_list, loan_balance_list, equity_list

    def income_statement(self):
        """ Returns a dictionary with all necessary values"""
        grossrent = self.rent
        annual_grossrent = grossrent * 12

        vacancy = self.rent * self.vacancy
        annual_vacancy = vacancy * 12

        annual_other_income = self.other_income * 12

        operating_income = self.get_operating_income()
        annual_operating_income = operating_income * 12

        operating_expenses = self.get_operating_expense()
        annual_operating_expenses = operating_expenses * 12

        noi = self.noi()
        annual_noi = noi * 12

        loan_payment = self.mortgage_payment()
        annual_loan_payment = loan_payment * 12

        cashflow = self.cashflow()
        annual_cashflow = cashflow * 12

        cf_dict = {'grossrent': comma_dollar(grossrent),
                   'annual_grossrent': comma_dollar(annual_grossrent),
                   'vacancy': comma_dollar(vacancy),
                   'annual_vacancy': comma_dollar(annual_vacancy),
                   'other_income': comma_dollar(self.other_income),
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

    def cash_flow_30_year(self, income_growth, expense_growth):
        year_list = []
        cash_flow_list = []
        annual_income = (self.rent) * 12
        annual_expense = (self.get_operating_expense() * 12)
        annual_debt_service = self.mortgage_payment() * 12
        float_income = 1 + (float(income_growth)/100)
        float_expense = 1 + (float(expense_growth)/100)

        for i in range(1, int(self.term)+1):
            annual_income = annual_income * float_income
            annual_vacancy = annual_income * self.vacancy
            annual_gross_income = annual_income - annual_vacancy
            annual_expense = annual_expense * float_expense
            cash_flow = round(annual_gross_income - annual_expense - annual_debt_service)
            year_list.append(i)
            cash_flow_list.append(cash_flow)
        return year_list, cash_flow_list

    def cap_rate(self):
        cap_rate = ((self.noi() * 12) / self.purchase_price) * 100

        if cap_rate < 0:
            return get_negative_percent(cap_rate)
        else:
            return get_percent(cap_rate)

    def cash_on_cash(self):
        coc = ((self.cashflow() * 12) / self.outofpocket()) * 100
        if coc < 0:
            return get_negative_percent(coc)
        else:
            return get_percent(coc)


def get_negative_percent(num):
    num = round(abs(num), 1)
    return "(" + str(num) + "%)"


def get_percent(num):
    num = round(num, 1)
    return str(num) + "%"


def handle_comma(number):
    if ',' in number:
        return number.replace(',', '')
    else:
        return str(number)


def comma_dollar(number):
    """ Adds comma and dollar sign to input string
    """
    num = int(number)
    if num < 0:
        payment_1 = format(round(num * -1), ',d')
        str_payment = "($" + str(payment_1) + ")"
        return str_payment
    else:
        payment_1 = format(round(num,2), ',d')
        str_payment = "$" + str(payment_1)
        return str_payment


def remove_comma_dollar(number):
    return number.replace(',', '').replace('$','')
