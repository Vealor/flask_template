
from functools import reduce

class ParedownRule:

    def __init__(self, paredown_conditions, code, comment=None):
        self.paredown_conditions = paredown_conditions
        self.code = code
        self.comment = comment

    def apply_to_data(self, df):
        fields_functions = [(pc.field_name,pc.get_evaluator()) for pc in self.paredown_conditions]
        return reduce(lambda x,y: x & y, [df[ff[0]].apply(ff[1]) for ff in fields_functions])
