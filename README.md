# FarmGPT-Formula-Backend

## Environment
- Python 3.9.16

## Setup



1. Write ```./config.json```
    - copy ```./config.json.example``` and rename it to ```./config.json```
    - fill in the values

2. Copy ```./data/formula_table.example.json``` and rename it to ```./data/formula_table.json```
    - If you have your own formula table, skip this step

3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Run (Development)

```bash
python app.py
```

## Add new formula

1. Add new formula to your own file which format like ```./data/formula_template.md```
    - Example:
        ```markdown
        ===

        ---
        illustrate:
        {description about this formula}

        ---

        formula:

        {math formula display with latex, and input variable name should like "x_1, x_2"}
        example: $out = x_1 + x_2$

        ---
        variable:
        {description about variable}
        example:

        $x_1$ = Description about $x_1$

        $x_2$ = Description about $x_2$

        ---
        chore:

        {other information about this formula that might be useful in the future} 

        ---
        variable_name:

        {the real variable name in the formula}
        example:

        $x_1$ = $C_{I}(i)$

        $x_2$ = $R_{K}(i)$

        ---

        ===
        ```

2.  ```bash
    python ./add_formula_to_table.py --data_path <your own file>
    ```





