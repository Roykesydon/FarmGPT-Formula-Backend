import re
from dataclasses import dataclass


class FormulaHandler:
    @dataclass
    class Detail:
        illustrate: str
        formula: str
        variable: dict
        variable_name: dict
        chore: str
        chatgpt_program_response: str
        calc_formula: str

    def __init__(self, model):
        self._formula_detail_list = []
        self.model = model

    def _get_compute_program_from_response(self, response: str) -> str:
        pattern = r"```python(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)

        if matches:
            return matches[0]
        elif "def" in response:
            return response

    def _get_method_part_from_python_program(self, python_program: str) -> str:
        python_program = python_program.split("\n")

        method_start = -1
        method_end = -1

        for i, line in enumerate(python_program):
            if line.strip().startswith("def"):
                method_start = i
            elif method_start != -1 and line.strip().startswith("return"):
                method_end = i
                break

        python_program = "\n".join(python_program[method_start : method_end + 1])
        return python_program

    def set_formula_detail_list_from_file(self, formula_file_path: str):
        self._formula_detail_list = []
        with open(formula_file_path, encoding="utf-8") as formula_file:
            # Read formula file
            lines = formula_file.readlines()
            lines = "".join(lines)

            formulas = lines.split("===")
            formulas = [formula.strip() for formula in formulas if len(formula)]

            # Transform formula to detail as dict
            for formula in formulas:
                details = formula.split("---")
                details = [detail.strip() for detail in details if len(detail)]

                formula_detail = {}
                for detail in details:
                    key, value = detail.split(":", 1)
                    formula_detail[key.strip()] = value.strip()

                formula_detail = self._detail_value_transform(formula_detail)

                self._formula_detail_list.append(formula_detail)

    def _detail_value_transform(self, detail: dict):
        # get detail data
        illustrate = detail["illustrate"]
        formula = detail["formula"]
        chore = detail["chore"]

        variable = self._equation_split(detail["variable"])
        variable = {
            self._regularize_x_variable_name(key): value
            for key, value in variable.items()
        }

        variable_name = self._equation_split(detail["variable_name"])
        variable_name = {
            self._regularize_x_variable_name(key): value
            for key, value in variable_name.items()
        }

        # get ChatGPT program reponse for formula
        if "chatgpt_program_response" in detail:
            chatgpt_program_response = detail["chatgpt_program_response"]
        else:
            # generate response from LLM
            prompt = f"""
formula:

{detail["formula"]}

---

幫我根據上面的公式生出python計算程式碼，只要給我method，透過parameters輸入變數數字
            """

            chatgpt_program_response = self.model.generate_response(prompt)
            chatgpt_program_response = chatgpt_program_response["choices"][0][
                "message"
            ]["content"]
            # chatgpt_program_response = (
            #     "def delta_c(x1, x2, x3, x4):\n    return (x2 - x1) / (x3 - x4)"
            # )

        try:
            # generate formula_program from response
            calc_formula = self._get_compute_program_from_response(
                chatgpt_program_response
            )
            calc_formula = self._get_method_part_from_python_program(calc_formula)
            calc_formula_before_method_name = "def "
            calc_formula_after_method_name = "(" + calc_formula.split("(", 1)[1]

            METHOD_NAME = "calc_formula"
            # regularize method parameter names
            (
                parameter_names,
                calc_formula_after_parameter,
            ) = calc_formula_after_method_name.split(")", 1)
            calc_formula_after_parameter = ")" + calc_formula_after_parameter
            parameter_names = self._regularize_x_variable_name(parameter_names)

            calc_formula = (
                calc_formula_before_method_name
                + METHOD_NAME
                + parameter_names
                + calc_formula_after_parameter
            )
        except Exception as e:
            calc_formula = "generate formula program failed"

        detail = self.Detail(
            illustrate=illustrate,
            formula=formula,
            variable=variable,
            variable_name=variable_name,
            chore=chore,
            chatgpt_program_response=chatgpt_program_response,
            calc_formula=calc_formula,
        )

        return detail

    def _regularize_x_variable_name(self, str):
        return str.replace("_", "")

    def _equation_split(self, equation: str) -> dict:
        equation = [
            equation.strip() for equation in equation.split("\n") if len(equation)
        ]
        equation = [
            equation_detail.replace("$", "").split("=") for equation_detail in equation
        ]
        equation = {left.strip(): right.strip() for left, right in equation}
        return equation

    def get_formula_detail_list(self):
        return self._formula_detail_list


if __name__ == "__main__":
    formula_handler = FormulaHandler()
    formula_handler.set_formula_detail_list_from_file("./formula.txt")
    print(formula_handler.get_formula_detail_list()[0].formula)
