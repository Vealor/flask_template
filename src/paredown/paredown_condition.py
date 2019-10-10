class ParedownCondition():

    def __init__(self, field_name, operator, value):

        self.field_name = field_name         #The data field name
        self.operator = operator        #The operator between
        self.value = value              #The value that the data field is compared to
        if self.operator in ['>','<','==','>=','<=','<>']:
            self.value_type = 'float'
        else:
            self.value_type = 'str'
            self.value = '"' + self.value + '"'
            if self.operator == 'contains':
                self.operator = 'in'

        self.evaluator = eval('lambda x : True if x ' + str(self.operator) + ' ' + str(self.value) + ' else False')


    def get_evaluator(self):
        return self.evaluator
