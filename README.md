## 免责声明

**请注意：** 本工具仅供学习和研究使用，不得用于任何商业用途或违反平台规定的活动。使用者应自行承担使用本工具可能产生的一切责任和后果。
本工具的开发者不承担任何因使用本工具而导致的任何直接或间接损失、责任或问题。使用者在使用本工具前，应确保已充分了解相关法律法规和平台规定，并承诺合法合规使用。
本工具不鼓励任何形式的作弊行为，使用者应尊重平台规则，维护良好的学习环境。

另外本项目仅能爬取已经做过的习题与试卷, 爬取的内容仅供期末期中复习使用

## 使用方法

### 环境要求

- Python 3.x
- 必要的Python库（见requirements.txt）

### 安装步骤

1. 克隆或下载本仓库到本地
2. 安装必要的依赖库：
   ```
   pip install -r requirements.txt
   ```

### 功能说明

本项目包含以下主要功能：

1. **cookies_to_json.py** - 处理Cookie转换
2. **final_exam.py** - 期末考试试卷(需要已经做过)相关功能
3. **main.py** - 主程序入口, 爬取单元习题答案(需要已经做过)

### 使用示例

#### 基本使用
先在浏览器复制cookies, 需要json格式,粘贴进main.py中,补全cookies变量的值
想获取json格式的cookies可以运行cookies_to_json.py,将纯文本的cookies转换成json格式
还有其他参数详见main.py
然后运行主程序：
```
python main.py
```

期末试卷需自己获取到期末试卷的object json数据,粘贴进test.json, 然后运行 final_exam.py
```
python final_exam.py
```
输出在./dist目录下

#### 各模块说明

1. **Cookie处理模块** (cookies_to_json.py)
   - 将浏览器Cookie转换为JSON格式
   - 使用方法：`python cookies_to_json.py`

2. **期末考试模块** (final_exam.py)
   - 获取期末考试试卷(已经做过)
   - 使用方法：`python final_exam.py`

3. **主程序** (main.py)
   - 爬取单元习题答案(已经做过)
   - 使用方法：`python main.py`

### 注意事项

1. 请确保在使用前已阅读并理解所有免责声明
2. 请遵守相关法律法规和平台规定


