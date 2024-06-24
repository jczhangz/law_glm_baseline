import json


class CompanyInfo:
    def __init__(self,公司名称:str):
        self.公司名称 = 公司名称
        pass


if __name__ == '__main__':
    # companyinfo = CompanyInfo('武汉')
    # print(companyinfo.公司名称)
    json_str = '{\'公司名称\': \'广州发展集团股份有限公司\'}'
    person = json.loads(json_str)
    person['公司名称']