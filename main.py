import time
import json
import logging
import os
from typing import List, Dict, Any, Optional

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ---------- 参数配置----------
cookies = {
    # your cookie here
}
class_front_code = '' # 课程编号 如'66115'
class_code = '' # 班级编号 如'14925761'
code_start = 20 # 起始章节
code_end = 100 # 结束章节
#---------------------------

def generate_padded_list(start: int, end: int, width: int = 2) -> List[str]:
    return [str(i).zfill(width) for i in range(start, end + 1)]


def create_session_with_retry(retries=3, backoff=1.0) -> requests.Session:
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_json(url: str, session: requests.Session, timeout=30) -> Optional[Dict]:
    try:
        resp = session.get(url, cookies=cookies, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.error(f"请求失败 {url}: {e}")
        return None


# ---------- 主逻辑 ----------
def main():
    code_list = generate_padded_list(code_start, code_end)
    session = create_session_with_retry()
    output_file = "./dist/xuetangzaixian.txt"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    index = 1
    with open(output_file, "w", encoding="utf-8") as f:
        for code in code_list:
            url = f'https://www.xuetangx.com/api/v1/lms/exercise/get_exercise_list/{class_front_code}{code}/{class_code}/'
            logger.info(f"处理章节 {code}: {url}")

            data = fetch_json(url, session)
            if not data:
                logger.warning(f"章节 {code} 数据获取失败，跳过")
                time.sleep(1)
                continue

            problems = data.get('data', {}).get('problems', [])
            if not problems:
                logger.info(f"章节 {code} 无题目")
                time.sleep(1)
                continue

            for problem in problems:
                try:
                    content = problem.get('content', {})
                    options = content.get('Options', [])
                    problem_type = content.get('TypeText', '未知')
                    difficulty = content.get('difficulty', '未知')

                    f.write(f"{problem_type}\n difficulty:{difficulty}\n")

                    # 解析题目正文
                    body_html = content.get('Body', '')
                    soup = BeautifulSoup(body_html, "html.parser")
                    if problem_type == '判断题':
                        problem_body = soup.get_text(strip=True)
                    else:
                        p = soup.find('p')
                        problem_body = p.get_text(strip=True) if p else soup.get_text(strip=True)

                    f.write(f"{index}.{problem_body}\n")
                    index += 1

                    # 写入选项
                    for opt in options:
                        key = opt.get('key', '')
                        val = opt.get('value', '')
                        opt_text = BeautifulSoup(val, "html.parser").get_text(strip=True)
                        f.write(f"\t{key}.{opt_text}\n")

                    # 写入答案
                    answers = problem.get('user', {}).get('answer', [])
                    f.write("answer:" + "".join(answers) + "\n\n")

                except Exception as e:
                    logger.error(f"处理题目时出错: {e}")
                    continue

            f.write("\n")
            f.flush()
            logger.info(f"章节 {code} 完成，当前总题数: {index - 1}")
            time.sleep(1)

    logger.info(f"全部完成！共 {index - 1} 道题目，保存至 {output_file}")


if __name__ == "__main__":
    main()