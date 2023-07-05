from dataclasses import dataclass

from flask import Blueprint, jsonify, request

from repository.DiskFormulaRepository import DiskFormulaRepository

formula_repository = DiskFormulaRepository("./data/formula_table.json")


input_variable_blueprints = Blueprint("input_variable", __name__)


@dataclass
class InputVariableData:
    name: str
    origin_name: str
    description: str
    formula_id: int
    class_id: int


@input_variable_blueprints.route("/", methods=["GET"])
def get_all_input_variable():
    # return all input variable in formula_table.json
    all_formula = formula_repository.return_all_formula()
    variable_list = []

    for formula in all_formula:
        variables_description = formula["variable"]
        variables_origin_name = formula["variable_name"]

        for variable, description in variables_description.items():
            origin_name = variables_origin_name[variable]
            formula_id = formula["id"]
            variable_list.append(
                InputVariableData(
                    name=variable,
                    origin_name=origin_name,
                    description=description,
                    formula_id=formula_id,
                    class_id=-1,
                )
            )

    return jsonify(variable_list)


@input_variable_blueprints.route("/match_formula", methods=["POST"])
def match_formula():
    # return fully matched or partially matched formula

    """
    output
    {
        "fully_matched": [
            {
                "formula_id": 1,
                "calculate_result": 7
            }
        ],
        "partially_matched": [
            {
                "formula_id": 2
            }
        ]
    }
    """

    return_json = {"fully_matched": [], "partially_matched": []}

    formula_dict = {}  # store variables to related formula

    # get post params
    varaibles_list = request.json

    # group variables by formula_id
    for variable_detail in varaibles_list:
        # regularize_x_variable_name
        name = variable_detail["name"].replace("_", "")

        formula_id = int(variable_detail["formula_id"])
        value = float(variable_detail["value"])

        formula_dict[formula_id] = formula_dict.get(formula_id, {})
        formula_dict[formula_id][name] = value

    # check if formula is fully matched or partially matched
    for formula_id, variable_value_dict in formula_dict.items():
        fully_match_flag = True

        formula_detail = formula_repository.get_formula_detail(formula_id)
        need_variables = []

        # check if all variables are matched
        for variable, _ in formula_detail["variable"].items():
            if variable not in variable_value_dict:
                fully_match_flag = False
                need_variables.append(variable)

        if fully_match_flag:
            # calculate result

            # get formula calculated program
            formula_detail = formula_repository.get_formula_detail(formula_id)
            formula_calc_program = formula_detail["calc_formula"]

            print(formula_calc_program)
            # calculate formula result
            exec(formula_calc_program, globals())
            result = calc_formula(**variable_value_dict)

            return_json["fully_matched"].append(
                {"formula_id": formula_id, "compute_result": str(result)}
            )

        elif not fully_match_flag:
            return_json["partially_matched"].append(
                {"formula_id": formula_id, "need_variables": need_variables}
            )

    return return_json
