
## API Document

### 公式

URL 前墜是 /formula

- URL：`/`
    - 說明：取得所有公式的資訊
    - 方法：GET
    - 參數：
    - 回傳：
        - 格式：JSON (list 包著)

        - | 參數名稱 | 類型   | 描述       |
            |----------|--------|------------|
            | formula   | string   | 公式本身 |
            | id   | int      | 每個公式的唯一 id |
            | illustrate   | string   | 公式的說明 |
            | variable   | dict (type A)   | 變數的相關資訊 |

            - type A
                - | 參數名稱 | 類型   | 描述       |
                    |----------|--------|------------|
                    | class_id   | int   | 變數對應到的類別 id |
                    | description   | string      | 變數的說明 |
                    | original_name   | string   | 變數原本的名字 |

        - 回傳範例：
            - ```json
                [
                    {
                        "formula": "DSOC=$x_1$×$x_2$×$x_3$×0.1",
                        "id": 1,
                        "illustrate": "土壤容重和土层深度来源于文献，若文献中未说明，容重根据 土壤质地在《中国土种志》[11~16]查得，土层深度默认 为 20 cm。\nDSOC = 农田土壤有机碳密度，tC·ha^-1",
                        "variable": {
                            "x1": {
                                "class_id": -1,
                                "description": "为土壤有机碳量(gC·kg^-1);",
                                "original_name": "SOC"
                            },
                            "x2": {
                                "class_id": -1,
                                "description": "为耕层土壤容重(g·cm^-3);",
                                "original_name": "γ"
                            },
                            "x3": {
                                "class_id": -1,
                                "description": "为土层深度(cm)。",
                                "original_name": "TH"
                            }
                        }
                    }
                ]
                ```

- URL：`/<int:formula_id>`
    - 說明：根據 id 取得公式的資訊
    - 方法：GET
    - 參數：
    - 回傳：
        - 格式：JSON

        - | 參數名稱 | 類型   | 描述       |
            |----------|--------|------------|
            | formula   | string   | 公式本身 |
            | id   | int      | 每個公式的唯一 id |
            | illustrate   | string   | 公式的說明 |
            | variable   | dict (type A)   | 變數的相關資訊 |

            - type A
                - | 參數名稱 | 類型   | 描述       |
                    |----------|--------|------------|
                    | class_id   | int   | 變數對應到的類別 id |
                    | description   | string      | 變數的說明 |
                    | original_name   | string   | 變數原本的名字 |

        - 回傳範例：
            - ```json
                {
                    "formula": "DSOC=$x_1$×$x_2$×$x_3$×0.1",
                    "id": 1,
                    "illustrate": "土壤容重和土层深度来源于文献，若文献中未说明，容重根据 土壤质地在《中国土种志》[11~16]查得，土层深度默认 为 20 cm。\nDSOC = 农田土壤有机碳密度，tC·ha^-1",
                    "variable": {
                        "x1": {
                        "class_id": -1,
                        "description": "为土壤有机碳量(gC·kg^-1);",
                        "original_name": "SOC"
                        },
                        "x2": {
                        "class_id": -1,
                        "description": "为耕层土壤容重(g·cm^-3);",
                        "original_name": "γ"
                        },
                        "x3": {
                        "class_id": -1,
                        "description": "为土层深度(cm)。",
                        "original_name": "TH"
                        }
                    }
                }
                ```

- URL：`/<int:formula_id>/calculate`
    - 說明：給予公式變數數值，後端計算結果
    - 方法：POST
    - 參數：
        - 格式：JSON
        - | 參數名稱 | 類型    | 描述       |
            |----------|---------|------------|
            | variables   | dict (type A)  | 存放使用者填的變數數值 |
            - tpye A 
                | 參數名稱 | 類型    | 描述       |
                |----------|---------|------------|
                | x(number)  | float  | 存放不同變數名稱和對應的數值 |
        - 範例：
            - ```json
                {
                    "variables":{
                        "x1": 3,
                        "x2": 9,
                        "x3": 7
                    }
                }
                ```
    - 回傳
        - 格式：JSON

        - | 參數名稱 | 類型  | 必定出現 | 描述       |
            |----------|------|---|------------|
            | compute_result   | string  | 是 | 計算結果 |
            | error_message   | string  | 否 | 若有錯誤，該欄會有錯誤訊息 |

            - error_message
                - "分母是 0"
                - "輸入變數資訊有誤"
                - "未知錯誤"
        - 回傳範例：
            - ```json
                {
                    "compute_result": "0.8571428571428571",
                }
                ```
            - ```json
                {
                    "compute_result": "",
                    "error_message": "輸入變數資訊有誤"
                }
                ```

### 輸入變數

URL 前墜是 /input_variable

- URL：`/`
    - 說明：取得所有輸入變數的資訊
    - 方法：GET
    - 參數：
    - 回傳：
        - 格式：JSON (list 包著)

        - | 參數名稱 | 類型   | 描述       |
            |----------|--------|------------|
            | class_id   | int   | 變數對應的唯一類別 id，-1 代表未分類|
            | description   | string | 變數的說明資訊 |
            | formula_id   | int   | 變數對應的唯一公式 id |
            | name   | string   | 變數的名稱 |
            | origin_name   | string   | 變數原本對應的名稱 |

        - 範例：
            - ```json
                [
                    {
                        "class_id": -1,
                        "description": "为土壤有机碳量(gC·kg^-1);",
                        "formula_id": 1,
                        "name": "x1",
                        "origin_name": "SOC"
                    },
                    {
                        "class_id": -1,
                        "description": "为耕层土壤容重(g·cm^-3);",
                        "formula_id": 1,
                        "name": "x2",
                        "origin_name": "γ"
                    }
                ]
                ```

- URL：`/match_formula`
    - 說明：給予一堆輸入變數和對應數值，回傳那些公式已經有完整的輸入資訊，哪些有部分的輸入資訊
    - 方法：POST
    - 參數：
        - 格式：JSON (list 包著)
        - | 參數名稱 | 類型    | 描述       |
            |----------|--------|-------------|
            | name   | string   | key 是參數的個別名字，value 是使用者填的數值 |
            | formula_id | int | 變數所在的公式唯一 id |
            | value | float | 變數的數值 |
        - 範例：
            - ```json
                [
                    {
                        "name": "x1",
                        "formula_id": 1,
                        "value": 3
                    },
                    {
                        "name": "x2",
                        "formula_id": 1,
                        "value": 4
                    }
                ]
                ```
    - 回傳
        - 格式：JSON

        - | 參數名稱 | 類型  | 必定出現 | 描述       |
            |----------|------|---|------------|
            | fully_matched   | list(type A)  | 是 | 給予的變數已經完全符合公式要求，會回傳公式 id 和計算結果 |
            | partially_matched   | list(type B)  | 是 | 有出現使用者給予的變數，但不足以計算結果的公式 |

            - list (type A)
                - | 參數名稱 | 類型   | 描述       |
                    |----------|------|------------|
                    | formula_id   | int | 公式對應的 id |
                    | calculate_result   | str   | 計算結果 |
            - list (type B)
                - | 參數名稱 | 類型   | 描述       |
                    |----------|------|------------|
                    | formula_id   | int | 公式對應的 id |
        - 回傳範例：
            - ```json
                {
                    "fully_matched": [
                        {
                            "compute_result": "-0.2",
                            "formula_id": 1
                        }
                    ],
                    "partially_matched": [
                        {
                            "formula_id": 2,
                            "need_variables": [
                                "x2"
                            ]
                        }
                    ]
                }
                ```

- URL：`/class`
    - 說明：取得所有輸入變數的分類表資訊
    - 方法：GET
    - 參數：
    - 回傳：
        - 格式：JSON

        - | 參數名稱 | 類型   | 描述       |
            |----------|--------|------------|
            | (class id)   | dict (type A)  | 包含對應的 class 資訊 |
            
            - type A
                - | 參數名稱 | 類型   | 描述       |
                    |----------|--------|------------|
                    | name   | string  | 分類的名稱 |

        - 範例：
            - ```json
                {
                    "1": {
                        "name": "Class A"
                    },
                    "2": {
                        "name": "Class B"
                    },
                    "3": {
                        "name": "Class C"
                    }
                }
                ```

- URL：`/class/<int:class id>`
    - 說明：根據 class id 回傳對應的 class 詳細資訊
    - 方法：GET
    - 參數：
    - 回傳：
        - 格式：JSON

            - | 參數名稱 | 類型   | 描述       |
                |----------|--------|------------|
                | name   | string  | 分類的名稱 |

        - 範例：
            - ```json
                {
                    "name": "Class A"
                }
                ```