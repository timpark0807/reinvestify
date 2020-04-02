from realtoranalysis.calculator.functions import remove_comma
from realtoranalysis.scripts.property_calculations import Calculate, comma_dollar, remove_comma_dollar
import secrets


def get_kwargs(request_object):
    temp = dict()
    temp['share'] = secrets.token_hex(8)

    for key, value in request_object.items():
        if key == 'title' and len(value) == 0:
            temp[key] = 'Untitled'
        elif key in {'sqft', 'bed', 'bath', 'year'} and len(value) == 0:
            temp[key] = '-'
        else:
            if key == 'price':
                temp['report_price'] = comma_dollar(remove_comma(value))
            temp[key] = remove_comma(value)

    property = Calculate(temp['price'],
                         temp['down'],
                         temp['interest'],
                         temp['term'],
                         temp['rent'],
                         temp['expenses'],
                         temp['vacancy'],
                         temp['closing'],
                         temp['other']
                         )

    temp['cash_flow'] = comma_dollar(property.cashflow())
    temp['cap_rate'] = property.cap_rate()
    temp['coc'] = property.cash_on_cash()

    return temp


def get_share_url(post_id, share):
    return ''.join(["http://www.reinvestify.com/analyze/", post_id, '/', share])


def get_data(post):

    share_url = get_share_url(str(post.id), str(post.share))

    property = Calculate(post.price,
                         post.down,
                         post.interest,
                         post.term,
                         post.rent,
                         post.expenses,
                         post.vacancy,
                         post.closing,
                         post.other
                         )

    mortgage_payment = property.mortgage_payment()
    out_of_pocket = property.outofpocket()
    vacancy_loss = property.get_vacancy_loss()
    operating_income = property.get_operating_income()
    operating_expense = property.get_operating_expense()
    noi = property.noi()
    cash_flow = property.cashflow()
    cap_rate = property.cap_rate()
    coc = property.cash_on_cash()

    # 30 year appreciation, equity, loan
    model_year, model_appreciation, model_loan, model_equity = property.appreciation_model(post.appreciation)

    # 30 year cash flow
    bar_year, bar_rent = property.cash_flow_30_year(post.income_growth, post.expense_growth)

    # cash flow table
    cashflow_data = property.income_statement()

    data = {'model_year': model_year,
            'model_appreciation': model_appreciation,
            'model_loan': model_loan,
            'model_equity': model_equity,
            'bar_year': bar_year,
            'bar_rent': bar_rent,
            'price': comma_dollar(float(post.price)),
            'mortgage': comma_dollar(mortgage_payment),
            'outofpocket': comma_dollar(out_of_pocket),
            'cap_rate': cap_rate,
            'coc': coc,
            'operating_income': comma_dollar(operating_income),
            'operating_expense': comma_dollar(operating_expense),
            'cash_flow': comma_dollar(cash_flow),
            'noi': comma_dollar(noi),
            'vacancy': vacancy_loss,
            'pie_ma': (int(mortgage_payment) * 12),
            'pie_oe': remove_comma_dollar(cashflow_data['annual_operating_expenses']),
            'pie_cf': remove_comma_dollar(cashflow_data['annual_cashflow']),
            'share_url': share_url
            }

    return data, cashflow_data

    """
    TODO
        /analyze
        0. Refactor models
            -> Detail  : title, url, street, city, state, type, year, etc.
            -> Numbers : price, rent, term, down, interest, closing
            -> Metrics : cash on cash, cash flow, vacancy loss, operating income 
            
        1. Pass the form inputs to the database as a hashtable (kwargs = dict(), pass in **kwargs) // DONE
            -> Have to manually add a 'report_price' in get_form_dict() method // DONE 
        2. Build input validator for each step of the form
        3. Check if report details are empty // Done 
        4. Calculate all metrics and store them in a metrics table when we submit our report
    
        
        /analyze/report 
        1. Create function that builds the data hashtable // DONE
            -> refactor all 3 routes 
                  /anaylze/<post_id> // DONE
                  /analyze/<post_id>/anon // DONE
                  /analyze/<post_id>/<share> // DONE
                  
        2. Create function that builds share_url // Done 
        
         
    """

