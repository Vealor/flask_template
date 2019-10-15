import re
re.search(r'\babc\b', 'abc 123')

class ParedownCondition():

    def __init__(self, field_name, operator, value):

        self.field_name = field_name         #The data field name
        self.operator = operator            #The operator between
        self.value = value                  #The value that the data field is compared to
        if self.operator in ['>','<','==','>=','<=','!=']:
            self.value_type = 'float'
            lambda_func_str = 'lambda x : True if x {} {} else False'.format(self.operator, self.value)
        else:
            self.value_type = 'str'
            if self.operator == 'contains':
                lambda_func_str = 'lambda x : True if re.search(r\'{}\', x, re.IGNORECASE) else False'.format(self.value)
            else:
                lambda_func_str = 'lambda x : True if x {} {} else False'.format(self.operator, self.value)

        print(lambda_func_str)
        self.evaluator = eval(lambda_func_str)


    def get_evaluator(self):
        return self.evaluator
