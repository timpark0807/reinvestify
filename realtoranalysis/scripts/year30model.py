import pandas as pd
import numpy

initial_value = 100000
initial_rent = 1500
intial_expense = initial_rent * .5


appreciation = 1.04
rent_increase = 1.02



appreciated_value = initial_value
income = initial_rent


year_list = []
rent_list = []
appreciation_list = []
loan_balance_list = []
equity_list = []

monthly_mortgage = 429

downpayment = 20000
initial_loan = 80000
annual_amortization = 12 * monthly_mortgage

loan_balance = initial_loan


for i in range(1, 31):
    appreciated_value = round(appreciated_value * appreciation)
    income = round(income * rent_increase)

    loan_balance = round(numpy.pv((.05 / 12), 360-(12 * i), monthly_mortgage)*-1)


    print(appreciated_value-initial_value)
    equity = (initial_value - loan_balance + (appreciated_value-initial_value))


    year_list.append("year " + str(i))
    loan_balance_list.append(loan_balance)
    appreciation_list.append(appreciated_value)
    rent_list.append(income)
    equity_list.append(equity)

print(year_list)
print(loan_balance_list)
print(appreciation_list)
print(rent_list)
print(equity_list)