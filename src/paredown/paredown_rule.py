
from functools import reduce

class ParedownRuleObject:

    def __init__(self, paredown_conditions, code, comment=None):
        self.paredown_conditions = paredown_conditions
        self.code = code
        self.comment = comment

    def apply_to_data(self, df):
        try:
            # Check if paredown columns exist
            if not all([col in df.columns for col in [pdc.field_name for pdc in self.paredown_conditions]]):
                raise ValueError("Cannot apply rule. DataFrame does not contain at least one required field_name.")

            fields_functions = [(pc.field_name,pc.value_type,pc.evaluator) for pc in self.paredown_conditions]
            return reduce(lambda x,y: x & y, [df[ff[0]].astype(ff[1]).apply(ff[2]) for ff in fields_functions])
        except Exception as e:
            raise Exception("Applying paredown rule failed: {}".format(str(e)))
