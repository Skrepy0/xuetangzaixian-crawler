import json
import os
import logging
from typing import List, Dict, Any

from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def extract_text_from_html(html: str, default: str = "") -> str:
    """安全地将HTML转为纯文本，异常时返回默认值"""
    try:
        if not html:
            return default
        return BeautifulSoup(html, "html.parser").get_text(strip=True)
    except Exception:
        return default


def parse_problem(problem: Dict[str, Any]) -> Dict[str, Any]:
    """
    兼容两种JSON结构：
    1. 直接包含 Options, TypeText, Body, Answer
    2. 包含 content 子对象（如API返回格式）
    """
    # 如果有 content 字段，则取 content 内部
    if "content" in problem:
        content = problem["content"]
        options = content.get("Options", [])
        problem_type = content.get("TypeText", "未知题型")
        body_html = content.get("Body", "")
        answer_list = problem.get("user", {}).get("answer", [])
    else:
        options = problem.get("Options", [])
        problem_type = problem.get("TypeText", "未知题型")
        body_html = problem.get("Body", "")
        answer_list = problem.get("Answer", [])

    return {
        "options": options,
        "problem_type": problem_type,
        "body_html": body_html,
        "answer_list": answer_list
    }


def process_problem(problem: Dict[str, Any], index: int, f) -> int:
    """处理单道题目，写入文件，返回下一个索引"""
    try:
        data = parse_problem(problem)
        options = data["options"]
        problem_type = data["problem_type"]
        body_html = data["body_html"]
        answer_list = data["answer_list"]

        # 写入题型
        f.write(f"{problem_type}\n")

        # 解析题目正文
        if problem_type == "判断题":
            # 判断题：直接提取纯文本
            body_text = extract_text_from_html(body_html, "（无题目文本）")
        else:
            # 非判断题：尝试取第一个 <p> 标签内的文本，否则取整体文本
            try:
                soup = BeautifulSoup(body_html, "html.parser")
                p_tag = soup.find("p")
                if p_tag:
                    body_text = p_tag.get_text(strip=True)
                else:
                    body_text = soup.get_text(strip=True)
            except Exception:
                body_text = extract_text_from_html(body_html, "（题目解析失败）")

        f.write(f"{index}.{body_text}\n")

        # 写入选项
        for option in options:
            key = option.get("key", "")
            value_html = option.get("value", "")
            opt_text = extract_text_from_html(value_html, "（无选项文本）")
            f.write(f"\t{key}.{opt_text}\n")

        # 写入答案
        f.write("answer:" + "".join(answer_list) + "\n\n")

        logger.debug(f"已处理第 {index} 题，类型: {problem_type}")
        return index + 1

    except Exception as e:
        logger.error(f"处理第 {index} 题时出错: {e}，跳过该题")
        return index  # 索引不变，跳过该题


def main(input_file: str = "test.json", output_file: str = "./dist/final_exam.txt") -> None:
    """主函数：读取JSON，解析题目，输出文本"""
    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 读取JSON文件
    try:
        with open(input_file, "r", encoding="utf-8") as jf:
            decoded_json = json.load(jf)
    except FileNotFoundError:
        logger.error(f"文件不存在: {input_file}")
        return
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析失败: {e}")
        return
    except Exception as e:
        logger.error(f"读取文件失败: {e}")
        return

    # 提取题目列表
    problems = decoded_json.get("data", {}).get("problems", [])
    if not problems:
        logger.warning("未找到任何题目（data.problems为空）")
        return

    logger.info(f"共找到 {len(problems)} 道题目，开始处理...")

    index = 1
    with open(output_file, "w", encoding="utf-8") as f:
        for problem in problems:
            index = process_problem(problem, index, f)
            f.flush()  # 及时写入磁盘

    total_processed = index - 1
    logger.info(f"处理完成！成功处理 {total_processed} 道题目，结果保存至 {output_file}")


if __name__ == "__main__":
    # 可自定义输入输出路径
    main(input_file="test.json", output_file="./dist/final_exam.txt")