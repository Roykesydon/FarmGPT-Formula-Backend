from flask import Blueprint, jsonify, request
from copy import deepcopy

from data_handler.JsonHandler import JsonHandler
from formula.FormulaHandler import FormulaHandler
from model.ChatGPT import ChatGPT
from repository.DiskFormulaRepository import DiskFormulaRepository

LLM_PRICE_PER_1K_TOKENS = 0.002
LLM_MAX_CONTEXT_TOKENS_LENGTH = 4090

json_handler = JsonHandler()

"""
read config
"""
config = json_handler.return_json_as_dict(json_path="./config.json")


"""
set up chatgpt
"""
model = ChatGPT(
    price_per_1k_tokens=LLM_PRICE_PER_1K_TOKENS,
    max_context_tokens_length=LLM_MAX_CONTEXT_TOKENS_LENGTH,
)
ChatGPT.set_api_key(config["openai_api_key"])

formula_handler = FormulaHandler(model)
formula_repository = DiskFormulaRepository(formula_table_path="./data/formula_table.json", variable_class_table_path="./data/variable_class_table.json")


formula_blueprints = Blueprint("formula", __name__)

def _pop_unnecessary_info(formula):
    formula.pop("chore")
    formula.pop("chatgpt_program_response")
    formula.pop("calc_formula")

@formula_blueprints.route("/", methods=["GET"])
def get_all_formula():
    # return all formula in formula_table.json
    all_formula = formula_repository.return_all_formula()
    
    # filter some info in formula
    for formula in all_formula:
        _pop_unnecessary_info(formula)

    return jsonify(all_formula)


@formula_blueprints.route("/<int:formula_id>", methods=["GET"])
def get_formula_detail(formula_id):
    # return formula detail
    formula_detail = formula_repository.get_formula_detail(formula_id)

    # filter some info in formula
    _pop_unnecessary_info(formula_detail)

    return formula_detail


@formula_blueprints.route("/<int:formula_id>/calculate", methods=["POST"])
def compute_formula(formula_id):
    return_json = {"compute_result": ""}

    try:
        # get post params
        param_json = request.json
        varaibles_dict = param_json["variables"]
        # regularize_x_variable_name in varaibles_dict's key
        varaibles_dict = {
            key.replace("_", ""): value for key, value in varaibles_dict.items()
        }

        # get formula calculated program
        formula_detail = formula_repository.get_formula_detail(formula_id)
        formula_calc_program = formula_detail["calc_formula"]

        print(formula_calc_program)
        # calculate formula result
        exec(formula_calc_program, globals())
        result = calc_formula(**varaibles_dict)

        return_json["compute_result"] = str(result)

    except ZeroDivisionError as e:
        return_json["error_message"] = "分母是 0"
    except TypeError as e:
        return_json["error_message"] = "輸入變數資訊有誤"
    except Exception as e:
        return_json["error_message"] = "未知錯誤"

    finally:
        return return_json
