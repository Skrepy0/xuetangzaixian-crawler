import time

import requests
from bs4 import BeautifulSoup
import json

cookies = {
    # your cookies here
}
with (open("./dist/xuetangzaixian.txt", "w", encoding="utf-8") as f):
    code_list = ['06', '08', '09', '11', '12', '17', '19', '23', '27']
    index = 1
    for code in code_list:
        url = f'https://www.xuetangx.com/api/v1/lms/exercise/get_exercise_list/57768{code}/13182184/'
        response = requests.get(url, cookies=cookies)
        json_text = f"{response.text}"
        decoded_json = json.loads(json_text)
        for problem in decoded_json['data']['problems']:
            options = problem['content']['Options']
            problem_type = problem['content']['TypeText']
            difficulty = problem['content']['difficulty']
            s1 = f"{problem_type}\n difficulty:{difficulty}\n"
            f.write(s1)
            body = BeautifulSoup(problem['content']['Body'], "html.parser")
            if problem_type == '判断题':
                problem_body = body
            else:
                problem_body = body.find('p').get_text()
            f.write(f"{index}.{problem_body}\n")
            index += 1
            answer_list = problem['user']['answer']
            for option in options:
                op = BeautifulSoup(option['value'], "html.parser")
                op_text = "\t" + option["key"] + '.' + op.get_text() + '\n'
                f.write(op_text)
            f.write("answer:")
            for answer in answer_list:
                f.write(answer)
            f.write("\n\n")
            print(index)
        f.write("\n")
        time.sleep(1)
        print("此章节完毕")
