import argparse

from data_handler.JsonHandler import JsonHandler
from formula.FormulaHandler import FormulaHandler
from model.ChatGPT import ChatGPT
from repository.DiskFormulaRepository import DiskFormulaRepository

formula_repository = DiskFormulaRepository("./data/formula_table.json")

json_handler = JsonHandler()

LLM_PRICE_PER_1K_TOKENS = 0.002
LLM_MAX_CONTEXT_TOKENS_LENGTH = 4090

"""
get args
"""
parser = argparse.ArgumentParser()
parser.add_argument("--data_path", help="Specify the data path")

args, extra_args = parser.parse_known_args()
extra_args = dict(zip(extra_args[0::2], extra_args[1::2]))

data_path = args.data_path
if data_path is None:
    print("data_path is not specified")
    exit(1)

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


"""
add formula to formula table
might send request to ChatGPT
"""
formula_handler = FormulaHandler(model=model)
formula_handler.set_formula_detail_list_from_file(data_path)

formula_detail_list = formula_handler.get_formula_detail_list()


for formula_detail in formula_detail_list:
    print(f"origin formula:\n\n{formula_detail.formula}")
    print("---")
    print(f"generated program:\n\n{formula_detail.calc_formula}")

    # client check if the formula program is correct
    client_answer = input("Is the formula program correct? (y/n)")
    if client_answer != "y":
        print("formula program is not correct, pass this one")
        continue

    formula_repository.add_formula(formula_detail)


"""
formula_handler = FormulaHandler()
formula_handler.set_formula_detail_list_from_file("./formula.txt")


json_handler = JsonHandler()
response = json_handler.return_json_as_dict("./output_1.json")
response_message = response["choices"][0]["message"]["content"]


def test():
    compute_program = "def delta_c(x1, x2, x3, x4):\n    return (x2 - x1) / (x3 - x4)"
    # print(compute_program)
    exec(compute_program, globals())
    print(delta_c(2, 5, 3, 4))


test()


# output formula_handler.get_formula_detail_list() result to a file
json_handler.save_json("formula_table.json", formula_handler.get_formula_detail_list())
"""
