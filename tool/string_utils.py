import re


def is_number(s):
    pattern = r'^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$'
    return bool(re.match(pattern, s))


def full_to_half(text):
    """
         全角括号转半角
        :param value:
        :param key
        :return: 公司名称: str
        """
    text = re.sub('（', '(', text)
    text = re.sub('）', ')', text)
    return text


def half_to_full(text: str):
    return text.replace('(', '（').replace(')', '）')

