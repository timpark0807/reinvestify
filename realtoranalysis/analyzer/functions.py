from realtoranalysis.calculator.functions import remove_comma


def get_form_dict(request_object):
    temp = {}
    for key, value in request_object.items():
        temp[key] = remove_comma(value)
    return temp

