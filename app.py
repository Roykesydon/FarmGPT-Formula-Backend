from flask import Flask, jsonify, request

from data_handler.JsonHandler import JsonHandler
from formula.FormulaHandler import FormulaHandler
from model.ChatGPT import ChatGPT
from repository.DiskFormulaRepository import DiskFormulaRepository

LLM_PRICE_PER_1K_TOKENS = 0.002
LLM_MAX_CONTEXT_TOKENS_LENGTH = 4090

json_handler = JsonHandler()

app = Flask(__name__)

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
formula_repository = DiskFormulaRepository("./data/formula_table.json")


@app.route("/formula", methods=["GET"])
def get_all_formula():
    # return all formula in formula_table.json
    return jsonify(formula_repository.return_all_formula())


@app.route("/formula/<int:formula_id>", methods=["GET"])
def get_formula_detail(formula_id):
    # return formula detail
    return formula_repository.get_formula_detail(formula_id)


@app.route("/formula/<int:formula_id>/calculate", methods=["POST"])
def compute_formula(formula_id):
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

        return str(result)
    except ZeroDivisionError as e:
        return "分母是 0"
    except TypeError as e:
        return "輸入變數資訊有誤"
    except Exception as e:
        return "Error"


if __name__ == "__main__":
    app.run(debug=True)
