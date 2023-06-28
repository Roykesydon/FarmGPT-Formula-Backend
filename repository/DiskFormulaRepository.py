import os
from dataclasses import asdict, dataclass

from data_handler.JsonHandler import JsonHandler
from repository.FormulaRepositoryInterface import FormulaRepositoryInterface


class DiskFormulaRepository(FormulaRepositoryInterface):
    def _need_backup(func):
        def wrapper(self, *args, **kwargs):
            try:
                self._create_backup()
                func(self, *args, **kwargs)
                self._delete_backup()
            except Exception as e:
                print(e)
                print("Error occurred, restore backup")
                self._restore_backup()

        return wrapper

    def __init__(self, formula_table_path: str) -> None:
        self._formula_table_path = formula_table_path
        self.json_handler = JsonHandler()
        self.formula_table = self.json_handler.return_json_as_dict(
            self._formula_table_path
        )
        for formula in self.formula_table:
            formula["calc_formula"] = formula["calc_formula"].replace("\\n", "\n")

    # override
    def return_all_formula(self) -> list:
        return self.formula_table

    # override
    def get_formula_detail(self, formula_id) -> dict:
        return self.formula_table[formula_id]

    # override
    @_need_backup
    def add_formula(self, add_formula: dataclass) -> None:
        # convert dataclass to dict
        add_formula = asdict(add_formula)

        # check replication
        for formula in self.formula_table:
            add_formula["id"] = formula["id"]
            if (
                formula["formula"] == add_formula["formula"]
                and formula["illustrate"] == add_formula["illustrate"]
            ):
                print("formula already exist")
                return

        max_id = 0
        for formula in self.formula_table:
            if formula["id"] > max_id:
                max_id = formula["id"]

        add_formula["id"] = max_id + 1
        self.formula_table.append(add_formula)

        self.json_handler.save_json(self._formula_table_path, self.formula_table)

    # override
    @_need_backup
    def delete_formula(self, formula_id: int) -> None:
        for formula in self.formula_table:
            if formula["id"] == formula_id:
                self.formula_table.remove(formula)
                break

        self.json_handler.save_json(self._formula_table_path, self.formula_table)

    def _create_backup(self) -> None:
        self.json_handler.save_json(
            self._formula_table_path + ".bak", self.formula_table
        )

    def _delete_backup(self) -> None:
        os.remove(self._formula_table_path + ".bak")

    def _restore_backup(self) -> None:
        self.formula_table = self.json_handler.return_json_as_dict(
            self._formula_table_path + ".bak"
        )
        self.json_handler.save_json(self._formula_table_path, self.formula_table)
