from config.constants import FUN_CALL_NAME_GET_COMPANY_REGISTER, \
    FUN_CALL_NAME_GET_COMPANY_INFO, FUN_CALL_NAME_SEARCH_COMPANY_NAME_BY_INFO, FUN_CALL_NAME_GET_LEGAL_DOCUMENT, \
    FUN_CALL_NAME_GET_SUB_COMPANY_INFO, FUN_CALL_NAME_SEARCH_COMPANY_NAME_BY_REGISTER, \
    FUN_CALL_NAME_SEARCH_CASE_NUM_BY_LEGAL_DOCUMENT, FUN_CALL_NAME_SEARCH_COMPANY_NAME_BY_SUB_INFO, \
    FUN_CALL_NAME_GET_COMPANY_FULL_NAME, FUN_CALL_NAME_GET_SUB_COMPANY_NAME_FIND_COMPANY_INFO, \
    FUN_CALL_NAME_GET_COMPANY_NAME_BY_INDUSTRY, FUN_CALL_NAME_LEGAL_INFO_BY_COMPANY_NAME
from config.logging_config import logger

COUNT_PROMPT = "你擅长统计,只返回数字，不给步骤，不要返回请注意，以json格式返回"
DEFAULT_PROMPT = "你是一名高级智能助手，你可以先对问题进行分类，问题类型只有法律案件咨询和上市公司数据查询两类。你擅长将问题分解，逐步得到最终答案，从文本中提取关键信息，精确、数据驱动，擅长统计，紧展示最终结果，无需展示过程。 投资和控股分别计算。 重点突出关键信息。 例如：江苏怡达化学股份有限公司。 不要造公司名字。如果有多个，请依次查询， 案号名称的规则提取出完整的案号,按号必须包含()和数字    将问题和答案结合后输出。注意不要输出“以上是符合条件的部分信息”。 "

web_search_tools = [
    {
        "type": "web_search",
        "web_search": {
            "enable": False,
            "search_result": False
        }
    }
]

tools = [
    {
        "type": "function",
        "function": {
            "name": FUN_CALL_NAME_GET_COMPANY_INFO,
            "description": "根据公司名称获取公司信息，包括公司名称、公司简介、英文名称、关联证券、公司代码、曾用简称、所属市场、所属行业、上市日期、法人代表、总经理、董秘、邮政编码、注册地址、办公地址、联系电话、传真、官方网址、电子邮箱、主营业务、经营范围、机构简介",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "description": "公司名称",
                        "type": "string"
                    }
                },
                "required": ["company_name"]
            },
        }
    },

    {
        "type": "function",
        "function": {
            "name": FUN_CALL_NAME_SEARCH_COMPANY_NAME_BY_INFO,
            "description": "根据公司简介、英文名称、关联证券、公司代码、曾用简称、所属市场、所属行业、上市日期、法人代表、总经理、董秘、邮政编码、注册地址、办公地址、联系电话、传真、官方网址、电子邮箱、主营业务、经营范围、机构简介 查询出公司名称",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "description": "参数名",
                        "type": "string"
                    },
                    "value": {
                        "description": "参数值",
                        "type": "string"
                    }
                },
                "required": ["key", "value"]
            },
        }
    },

    {
        "type": "function",
        "function": {
            "name": FUN_CALL_NAME_GET_COMPANY_REGISTER,
            "description": "根据公司名称查询注册信息，注册信息包含公司名称、登记状态、统一社会信用代码、注册资本、成立日期、省份、城市、区县、注册号、组织机构代码、参保人数、企业类型、曾用名",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "description": "公司名字",
                        "type": "string"
                    }
                },
                "required": ["company_name"]
            },
        }
    },

    {
        "type": "function",
        "function": {
            "name": FUN_CALL_NAME_SEARCH_COMPANY_NAME_BY_REGISTER,
            "description": "根据企业公司注册信息，公司名称、登记状态、统一社会信用代码、注册资本、成立日期、省份、城市、区县、注册号、组织机构代码、参保人数、企业类型、曾用名，查询公司名称",
            # "description": "根据公司注册信息某个字段是某个值来查询具体的公司名称",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "description": "参数名",
                        "type": "string"
                    },
                    "value": {
                        "description": "参数值",
                        "type": "string"
                    }
                },
                "required": ["key", "value"]
            },
        }
    },

    {
        "type": "function",
        "function": {
            "name": FUN_CALL_NAME_GET_SUB_COMPANY_INFO,
            "description": "根据公司名称获得与子公司有关的所有关联上市公司信息, 对子公司的投资额 比如：[控股比例份额,子公司名称,投资],并且根据结果统计投资和控股",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "description": "公司名字",
                        "type": "string"
                    }
                },
                "required": ["company_name"]
            },
        }
    },

    {
        "type": "function",
        "function": {
            "name": FUN_CALL_NAME_GET_SUB_COMPANY_NAME_FIND_COMPANY_INFO,
            "description": "根据子公司的名字找到它属于是哪一家企业集团公司下的子公司",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "description": "公司名字",
                        "type": "string"
                    }
                },
                "required": ["company_name"]
            },
        }
    },

    {
        "type": "function",
        "function": {
            "name": FUN_CALL_NAME_GET_LEGAL_DOCUMENT,
            "description": "根据案号获得该案所有基本信息，返回的信息包含标题、案号、文书类型、原告、被告、原告律师、被告律师、案由、审理法条依据、依据的法律条文、涉案金额、判决结果、胜诉方、文件名",
            "parameters": {
                "type": "object",
                "properties": {
                    "case_num": {
                        "description": "案号",
                        "type": "string"
                    }
                },
                "required": ["case_num"]
            },
        }
    },

    {
        "type": "function",
        "function": {
            "name": FUN_CALL_NAME_SEARCH_CASE_NUM_BY_LEGAL_DOCUMENT,
            "description": "根据标题、案号、文书类型、原告、被告、原告律师、被告律师、案由、审理法条依据、涉案金额、判决结果、胜诉方、文件名 来查询案号",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "description": "参数名",
                        "type": "string"
                    },
                    "value": {
                        "description": "参数值",
                        "type": "string"
                    }
                },
                "required": ["key", "value"]
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": FUN_CALL_NAME_GET_COMPANY_NAME_BY_INDUSTRY,
            "description": "根据所属行业查询行业下的所有公司的注册信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "description": "参数名",
                        "type": "string"
                    },
                    "value": {
                        "description": "参数值",
                        "type": "string"
                    }
                },
                "required": ["key", "value"]
            },
        }
    },

    {
        "type": "function",
        "function": {
            "name": FUN_CALL_NAME_LEGAL_INFO_BY_COMPANY_NAME,
            "description": "根据公司名称查询被告信息合作的律师事务所",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "description": "公司名字",
                        "type": "string"
                    }
                },
                "required": ["company_name"]
            },
        }
    },

    {
        "type": "function",
        "function": {
            "name": FUN_CALL_NAME_GET_COMPANY_NAME_BY_INDUSTRY,
            "description": "根据所属行业查询行业下的所有公司",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "description": "参数名",
                        "type": "string"
                    },
                    "value": {
                        "description": "参数值",
                        "type": "string"
                    }
                },
                "required": ["key", "value"]
            },
        }
    }

]
