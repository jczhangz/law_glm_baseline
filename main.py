from config.logging_config import logger
import json
import argparse
from tool.file_processor import read_jsonl
from model.zhipu.handler import get_answer
from datetime import date

logger.name = __name__


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--question_file_path', type=str, default='data/question.json', nargs='?',
                        help='question file which need predict')
    date_today = date.today()
    output_file_name = date_today.__str__() + "_result.json"
    parser.add_argument('--answer_file_path', type=str, default=f'data/{output_file_name}', nargs='?',
                        help='answer file which model generate')

    args = parser.parse_args()

    contents = read_jsonl(args.question_file_path)
    for i, content in enumerate(contents):
        answer = get_answer(content.get('question'))
        content['answer'] = answer
        with open(args.answer_file_path, 'a+', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False)
            f.write('\n')
        if i % 50 == 49:
            logger.info(f"已预测{i}条")
            print(f"已预测{i}条")
    print("预测完成！")


if __name__ == '__main__':
    main()
