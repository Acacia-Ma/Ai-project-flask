import inspect
import json
import pandas as pd
from zhipuai import ZhipuAI
from pprint import pprint
client_zhipu = ZhipuAI(api_key="dae4b7d3a476814fa8938ee5183045af.9UDOI9jvUOcpkHx2")  # 你自己的api key


# AutoFunctionGenerator 类用于自动生成一系列功能函数的 JSON Schema 描述。
class AutoFunctionGenerator:
    """
   AutoFunctionGenerator 类用于自动生成一系列功能函数的 JSON Schema 描述。
   该类通过调用 OpenAI API，采用 Few-Shot learning 的方式来生成函数的描述。

   属性:
   - function_list (list): 一个包含多个功能函数的列表。
   - max_attempts (int): 最大尝试次数,用于处理 API 调用失败的情况。默认值设为 3

   方法:
   - __init__ : 初始化 AutoFunctionGenerator 类
   - generate_function_description: 自动生成功能函数的 JSON Schema 描述
   - _call_openai_api: 调用 OpenAI API
   - auto_generate : 自动生成功能函数的 JSON Schema 描述，并处理任何异常情况
   """

    def __init__(self, functions_list, max_attempts=3):
        """
        初始化 AutoFunctionGenerator 类

        参数:
        - function_list (list): 一个包含多个功能函数的列表。
        - max_attempts (int): 最大尝试次数,用于处理 API 调用失败的情况。默认值设为 3
        """
        self.functions_list = functions_list
        self.max_attempts = max_attempts

    def generate_function_description(self):
        """
        自动生成功能函数的 JSON Schema 描述

        返回:
        - list: 包含 JSON Schema 描述的列表
        """
        # 创建空列表，用于每个功能函数的JSON Schema描述
        functions = []
        # 遍历功能函数列表
        for function in self.functions_list:
            # 读取指定函数的函数说明
            function_description = inspect.getdoc(function)
            # print("function_description:", function_description)
            # 读取函数的名称
            function_name = function.__name__
            # print("function_name:", function_name)
            # 定义system role的Few-shot提示
            system_Q = "你是一位优秀的数据分析师，现在有一个函数的详细声明如下：%s" % function_description
            system_A = "计算年龄总和的函数，该函数从一个特定格式的JSON字符串中解析出DataFrame，然后计算所有人的年龄总和并以JSON格式返回结果。"\
                       "\n:param input_json: 必要参数，要求字符串类型，表示含有个体年龄数据的JSON格式字符串 "\
                       "\n:return: 计算完成后的所有人年龄总和，返回结果为JSON字符串类型对象"

            # 定义user role的Few-shot提示
            user_Q = "请根据这个函数声明，为我生成一个JSON Schema对象描述。这个描述应该清晰地标明函数的输入和输出规范。具体要求如下："\
                     "1.JSON Schema对象中包含'type'和'function'两个字段，其中'type'设置为'function'，其他属性都在'function'字段中设置."\
                     "2. 提取函数名称：%s，并将其用作'function'字段中的'name'字段 "\
                     "3. 在'function'字段中，设置函数的参数类型为'object'."\
                     "4. 'properties'字段如果有参数，必须表示出字段的描述. "\
                     "5. 从函数声明中解析出函数的描述，并在'function'字段中以中文字符形式表示在'description'字段."\
                     "6. 识别函数声明中哪些参数是必需的，然后在'parameters'字段的'required'字段中列出这些参数. "\
                     "7. 输出的应仅为符合上述要求的JSON Schema对象内容,不需要任何上下文修饰语句. " % function_name
            user_A = (
                "{'type':'function',"
                "'function':{'name':'calculate_total_age_function','description': '计算年龄总和的函"
                "数，从给定的JSON格式字符串（按'split'方向排列）中解析出DataFrame，计算所有人的年龄总和，并以"
                "JSON格式返回结果。' "
                "'parameters': {'type': 'object', "
                "'properties': {'input_json': {'description': '执行计算年龄总和的数据集', 'type':"
                "'string'}},"
                "'required': ['input_json']}}"
            )
            system_message = "你是一位优秀的数据分析师，现在有一个函数的详细声明如下：%s" % function_description
            user_message = ("请根据这个函数声明，为我生成一个JSON Schema对象描述。这个描述应该清晰地标明函数的输"
                            "入和输出规范。具体要求如下："
                            "1.JSON Schema对象中包含'type'和'function'两个字段，其中'type'设置为'function'，其他属性"
                            "都在'function'字段中设置."
                            "2. 提取函数名称：%s，并将其用作'function'字段中的'name'字段 "
                            "3. 在'function'字段中，设置函数的参数类型为'object'."
                            "4. 'properties'字段如果有参数，必须表示出字段的描述. "
                            "5. 从函数声明中解析出函数的描述，并在'function'字段中以中文字符形式表示"
                            "在'description'字段."
                            "6. 识别函数声明中哪些参数是必需的，然后在'parameters'字段的'required'字段中列出"
                            "这些参数. "
                            "7. 输出的应仅为符合上述要求的JSON Schema对象内容,不需要任何上下文修饰语句,仅包含JSON Schema对象内容，只要纯代码，不要有任何注释。" % function_name
                            )
            messages = [
                {
                    "role": "system",
                    "content": "Q:" + system_Q + user_Q + "A:" + system_A + user_A
                },
                {
                    "role": "user",
                    "content": 'Q:' + system_message + user_message
                }
            ]
            response = self._call_openai_api(messages)
            # strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
            # response_content = response.choices[0].message.content.strip()

            # 打印响应内容用于调试
            # print("response:", response)
            # print(response.choices[0].message.content)
            # print('---------------3',response.choices[0].message.content)
            functions.append(json.loads(response.choices[0].message.content[7:-3]))
            # print('---------------------4')
            # print("functions:", functions)
        return functions

    def _call_openai_api(self, messages):
        """
            调用 OpenAI API(私有方法)

            参数:
            - messages (list): 包含 API 所需信息的消息列表

            返回:
            - response: API 调用的响应对象
        """
        # 向模型提问
        return client_zhipu.chat.completions.create(
            model="glm-4",
            messages=messages,
            top_p=0.7,
            temperature=0.9,
            stream=False,
            max_tokens=2000,
            # tools=tools,
            # 可以不设置
            # tool_choice="auto",
        )

    def auto_generate(self):
        """
        自动生成功能函数的 JSON Schema 描述，并处理任何异常情况

        返回:
        - list: 包含 JSON Schema 描述的列表

        异常：
        - 如果 达到最大尝试次数，将引发异常
        """
        attempts = 0
        while attempts < self.max_attempts:
            try:
                functions = self.generate_function_description()
                return functions
            except Exception as e:
                attempts += 1
                print(f"Error: {e}")
                print(f"Attempt {attempts} failed")
                if attempts >= self.max_attempts:
                    print("Max attempts reached. Exiting...")
                    raise e
                else:
                    print("Retrying...")
                    continue


# 定义消息列表
def calculate_total_age_function(input_json):
    """
    从给定的JSON格式字符串（按'split'方向排列）中解析出DataFrame，计算所有人的年龄总和，并以JSON格式返回结果。
    参数:
    input_json(str): 含有个体年龄数据的JSON格式字符串
    返回:
    str: 计算完成后的所有人年龄总和，返回结果为JSON字符串类型对象
    """

    # 将JSON字符串转换为DataFrame
    df = pd.read_json(input_json, orient='split')
    # 计算年龄总和
    total_age = df['Age'].sum()
    # 将计算结果转换为JSON字符串
    return json.dumps({"total_age": str(total_age)})


# 测试函数
def calculate_married_count(input_json):
    """
    从给定的JSON格式字符串（按'split'方向排列）中解析出DataFrame，计算所有已婚人数，并以JSON格式返回结果。
    参数:
    input_json(str): 含有个体年龄数据的JSON格式字符串
    返回:
    str: 计算完成后的所有已婚人数，返回结果为JSON字符串类型对象
    """

    # 将JSON字符串转换为DataFrame
    df = pd.read_json(input_json, orient='split')
    # 计算已婚人数
    married_count = df[df['IsMarried'] == True].shape[0]
    # 将计算结果转换为JSON字符串
    return json.dumps({'married_count': str(married_count)})


def get_flight_number(data: str, departure: str, destination: str):
    """
    从给定的JSON格式字符串（按'split'方向排列）中解析出DataFrame，根据始发地，目的地和日期，查询对应的航班号，并以JSON格式返回结果。
    参数:
    data (str): 出发日期
    departure (str): 始发地
    destination (str): 目的地
    返回:
    str: 查询到的航班号，返回结果为JSON字符串类型对象
    """
    flight_number = {
        "北京": {
            "上海": "1234",
            "广州": "8321",
        },
        "上海": {
            "北京": "1233",
            "广州": "8123",
        }
    }
    return json.dumps({"flight_number": flight_number[departure][destination]})


functions_list = [calculate_total_age_function, calculate_married_count, get_flight_number]
if __name__ == '__main__':
    # 创建函数生成器对象
    generator = AutoFunctionGenerator(functions_list)
    # 生成函数描述
    functions_description = generator.auto_generate()
    # 打印生成的函数描述
    print("最后的的结果为:")
    # print(functions_description)
    pprint(functions_description)
