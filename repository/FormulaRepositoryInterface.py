import abc


class FormulaRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def return_all_formula(self):
        "Return all formula in formula table"
        return NotImplemented

    @abc.abstractmethod
    def get_formula_detail(self, formula_id):
        "Return formula detail by formula id"
        return NotImplemented

    @abc.abstractmethod
    def add_formula(self, formula):
        "Add formula to formula table"
        return NotImplemented

    @abc.abstractmethod
    def delete_formula(self, formula_id):
        "Delete formula from formula table"
        return NotImplemented
    
    @abc.abstractmethod
    def return_all_variable_class(self):
        "Return all variable class"
        return NotImplemented
