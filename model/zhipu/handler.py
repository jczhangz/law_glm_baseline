from zhipuai import ZhipuAI
from config import constants
from config.constants import FUN_CALL_NAME_GET_COMPANY_REGISTER, \
    FUN_CALL_NAME_GET_COMPANY_INFO, FUN_CALL_NAME_SEARCH_COMPANY_NAME_BY_INFO, FUN_CALL_NAME_GET_LEGAL_DOCUMENT, \
    FUN_CALL_NAME_GET_SUB_COMPANY_INFO, FUN_CALL_NAME_SEARCH_COMPANY_NAME_BY_REGISTER, \
    FUN_CALL_NAME_SEARCH_CASE_NUM_BY_LEGAL_DOCUMENT, FUN_CALL_NAME_SEARCH_COMPANY_NAME_BY_SUB_INFO, \
    FUN_CALL_NAME_GET_COMPANY_FULL_NAME, FUN_CALL_NAME_GET_SUB_COMPANY_NAME_FIND_COMPANY_INFO, \
    FUN_CALL_NAME_GET_COMPANY_NAME_BY_INDUSTRY, FUN_CALL_NAME_LEGAL_INFO_BY_COMPANY_NAME
from config.logging_config import logger
import json
from tool.zhipu.http_tool import get_company_info, search_company_name_by_info, \
    get_company_register, search_company_name_by_register, get_sub_company_info, \
    search_company_name_by_sub_info, get_legal_document, search_case_num_by_legal_document
from prompt.prompt import tools, web_search_tools, COUNT_PROMPT, DEFAULT_PROMPT

from typing import List, Union

logger.name = __name__

client = ZhipuAI(api_key=constants.zhipu_key)


# 统计用
def get_count_model(content: str):
    messages = []
    messages.append({"role": "system", "content": COUNT_PROMPT})
    messages.append({"role": "user", "content": content})

    response = client.chat.completions.create(
        model=constants.model_glm_4_0520,  # 这里用0520做统计
        temperature=0.1,
        top_p=0.1,
        messages=messages,
        tools=web_search_tools
    )
    print(response.choices[0].message)
    print(
        f'pompt_tokens:{response.usage.prompt_tokens},completion_tokens:{response.usage.completion_tokens},total_tokens:{response.usage.total_tokens}')
    return response.choices[0].message.content


def get_answer(question: str):
    messages = []
    messages.append({"role": "system",
                     "content": DEFAULT_PROMPT})

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=constants.model_glm_4,  # 填写需要调用的模型名称
        temperature=0.95,
        top_p=0.7,
        messages=messages,
        tools=tools,
    )
    print(response.choices[0].message)
    messages.append(response.choices[0].message.model_dump())

    result = ""
    while True:
        if response.choices[0].message.tool_calls:
            result, response = parse_function_call(response, messages, tools, question)
        else:
            result = response.choices[0].message.content
            break

    return result


def parse_function_call(model_response, messages, tools, question):
    if model_response.choices[0].message.tool_calls:
        tool_call = model_response.choices[0].message.tool_calls[0]
        args = tool_call.function.arguments
        function_result = {}

        if tool_call.function.name == FUN_CALL_NAME_GET_COMPANY_INFO:
            function_result = get_company_info(**json.loads(args))

            if len(function_result) == 0:
                company_name = json.loads(args)['company_name']
                company_name_dict = search_company_name_by_info("公司简称", company_name)
                if len(company_name_dict):
                    function_result = get_company_info(company_name_dict['公司名称'])

        if tool_call.function.name == FUN_CALL_NAME_SEARCH_COMPANY_NAME_BY_INFO:

            function_result = search_company_name_by_info(**json.loads(args))
            # 模型抽的字段可能不对 用其他字段依次查询
            if len(function_result) == 0:
                param = json.loads(args)
                # 根据其他字段一次查询
                for company_info_property in constants.company_info_property_list:
                    key = company_info_property
                    value = param['value']
                    function_result = search_company_name_by_info(key, value)
                    if len(function_result) > 0:
                        break

        if tool_call.function.name == FUN_CALL_NAME_GET_COMPANY_REGISTER:
            register_info = get_company_register(**json.loads(args))

            if len(register_info) == 0:
                function_result = search_company_name_by_register('注册号', json.loads(args)['company_name'])
            else:
                function_result = register_info

        if tool_call.function.name == FUN_CALL_NAME_SEARCH_COMPANY_NAME_BY_REGISTER:
            function_result = search_company_name_by_register(**json.loads(args))

        if tool_call.function.name == FUN_CALL_NAME_GET_SUB_COMPANY_INFO:
            # 传的是母公司的名称，需要从母公司找到子公司
            sub_company_list = []

            for sub_company_info_property in constants.sub_company_info_property_list:
                key = sub_company_info_property
                value = json.loads(args)['company_name']
                company_name_list = []
                company_name = search_company_name_by_sub_info(key, value)

                if len(company_name_list) == 0:
                    company_name_str = json.loads(args)['company_name']
                    search_company_name = search_company_name_by_info('英文名称', company_name_str)

                    if len(search_company_name) > 0:
                        company_name = search_company_name_by_sub_info(key, search_company_name['公司名称'])

                if isinstance(company_name, dict):
                    company_name_list.append(company_name)

                if isinstance(company_name, List):
                    company_name_list = company_name

                if len(company_name_list) > 0:

                    for company_name_dict in company_name_list:
                        sub_company_info = get_sub_company_info(company_name_dict['公司名称'])
                        print(sub_company_info)
                        sub_company_info.pop('关联上市公司股票代码')
                        sub_company_info.pop('关联上市公司股票简称')
                        # sub_company_info.pop('关联上市公司全称')
                        sub_company_info.pop('上市公司关系')
                        if sub_company_info.get('上市公司参股比例'):
                            pass
                        else:
                            sub_company_info['上市公司参股比例'] = "0"

                        if sub_company_info.get('上市公司投资金额'):
                            pass
                        else:
                            sub_company_info['上市公司投资金额'] = "0万"

                        sub_company_info['子公司名称'] = sub_company_info['公司名称']
                        sub_company_info['控股'] = sub_company_info['上市公司参股比例']
                        sub_company_info['投资'] = sub_company_info['上市公司投资金额']

                        sub_company_info.pop('关联上市公司全称')
                        sub_company_info.pop('公司名称')
                        sub_company_info.pop('上市公司参股比例')
                        sub_company_info.pop('上市公司投资金额')

                        sub_company_list.append(sub_company_info)
                    break
            print(sub_company_list)
            content = sub_company_list.__str__() + " " + question
            content = get_count_model(content)

            # 小于30家公司 将数据给模型，大于30家公司直接给计算结果
            if len(sub_company_list) < 30:
                # 合并
                sub_company_list.append({"统计", content})
                function_result = sub_company_list
            else:
                function_result = content

        if tool_call.function.name == FUN_CALL_NAME_GET_LEGAL_DOCUMENT:
            function_result = get_legal_document(**json.loads(args))
        if tool_call.function.name == FUN_CALL_NAME_SEARCH_CASE_NUM_BY_LEGAL_DOCUMENT:
            case_num_info = search_case_num_by_legal_document(**json.loads(args))

            cas_num_list = []
            if isinstance(case_num_info, dict):
                cas_num_list.append(case_num_info)

            if isinstance(case_num_info, List):
                cas_num_list = case_num_info

            legal_info_list = []
            if len(case_num_info) != 0:
                for case_num in cas_num_list:
                    legal_info_list.append(get_legal_document(case_num['案号']))

            function_result = legal_info_list.__str__()

        if tool_call.function.name == FUN_CALL_NAME_GET_COMPANY_NAME_BY_INDUSTRY:
            param = json.loads(args)
            key = '所属行业'
            value = param['value']
            company_name_list = search_company_name_by_info(key, value)
            if len(company_name_list) > 0:
                register_info_list = []
                for company_name in company_name_list:
                    register_info = get_company_register(company_name['公司名称'])
                    register_info_list.append(register_info)

                register_info_list.append({"公司数量", len(register_info_list)})
                function_result = register_info_list

        if tool_call.function.name == FUN_CALL_NAME_GET_SUB_COMPANY_NAME_FIND_COMPANY_INFO:
            function_result = get_sub_company_info(**json.loads(args))

        if tool_call.function.name == FUN_CALL_NAME_LEGAL_INFO_BY_COMPANY_NAME:
            company_name = json.loads(args)['company_name']
            cas_num_result = search_case_num_by_legal_document('被告', company_name)
            cas_num_list = []
            legal_info_list = []

            if isinstance(cas_num_result, dict):
                cas_num_list.append(cas_num_result)

            if isinstance(cas_num_result, List):
                cas_num_list = cas_num_result

            for case_num in cas_num_list:
                legal_info_list.append(get_legal_document(case_num['案号']))

            function_result = legal_info_list.__str__()

        print(function_result)
        messages.append({
            "role": "tool",
            "content": function_result.__str__(),
            "tool_call_id": tool_call.id
        })
        response = client.chat.completions.create(
            model=constants.model_glm_4,  # 填写需要调用的模型名称
            messages=messages,
            tools=tools,
        )
        print(response.choices[0].message)
        print(
            f'pompt_tokens:{response.usage.prompt_tokens},completion_tokens:{response.usage.completion_tokens},total_tokens:{response.usage.total_tokens}')
        messages.append(response.choices[0].message.model_dump())

        return response.choices[0].message.content, response
