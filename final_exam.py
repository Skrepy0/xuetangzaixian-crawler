import json

from bs4 import BeautifulSoup

with open('test.json', 'r', encoding='utf-8') as jf:
    decoded_json = json.load(jf)
index = 1
with (open("./dist/final_exam.txt", "w", encoding="utf-8") as f):
    for problem in decoded_json['data']['problems']:
        options = problem['Options']
        problem_type = problem['TypeText']
        s1 = f"{problem_type}\n"
        f.write(s1)
        body = BeautifulSoup(problem['Body'], "html.parser")
        if problem_type == '判断题':
            problem_body = body
        else:
            problem_body = body.find('p').get_text()
        f.write(f"{index}.{problem_body}\n")
        index += 1
        answer_list = problem['Answer']
        for option in options:
            op = BeautifulSoup(option['value'], "html.parser")
            op_text = "\t" + option["key"] + '.' + op.get_text() + '\n'
            f.write(op_text)
        f.write("answer:")
        for answer in answer_list:
            f.write(answer)
        f.write("\n\n")
        print(index)
