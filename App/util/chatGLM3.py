import inspect
import json
import pandas as pd
from zhipuai import ZhipuAI
from pprint import pprint

client_zhipu = ZhipuAI(api_key="dae4b7d3a476814fa8938ee5183045af.9UDOI9jvUOcpkHx2")  # 你自己的api key
from .functionsList import calculate_total_age_function, calculate_married_count, get_flight_number, \
    fetch_latest_qqemail_content, send_email


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
            system_A = "计算年龄总和的函数，该函数从一个特定格式的JSON字符串中解析出DataFrame，然后计算所有人的年龄总和并以JSON格式返回结果。" \
                       "\n:param input_json: 必要参数，要求字符串类型，表示含有个体年龄数据的JSON格式字符串 " \
                       "\n:return: 计算完成后的所有人年龄总和，返回结果为JSON字符串类型对象"

            # 定义user role的Few-shot提示
            user_Q = "请根据这个函数声明，为我生成一个JSON Schema对象描述。这个描述应该清晰地标明函数的输入和输出规范。具体要求如下：" \
                     "1.JSON Schema对象中包含'type'和'function'两个字段，其中'type'设置为'function'，其他属性都在'function'字段中设置." \
                     "2. 提取函数名称：%s，并将其用作'function'字段中的'name'字段 " \
                     "3. 在'function'字段中，设置函数的参数类型为'object'." \
                     "4. 'properties'字段如果有参数，必须表示出字段的描述. " \
                     "5. 从函数声明中解析出函数的描述，并在'function'字段中以中文字符形式表示在'description'字段." \
                     "6. 识别函数声明中哪些参数是必需的，然后在'parameters'字段的'required'字段中列出这些参数. " \
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


functions_list = [calculate_total_age_function, calculate_married_count, get_flight_number,
                  fetch_latest_qqemail_content, send_email]

functions_dec = [
    {
        'type': 'function',
        'function': {
            'name': 'calculate_total_age_function',
            'description': '从给定的JSON格式字符串中解析出DataFrame，计算所有人的年龄总和，并以JSON格式返回结果。',
            'parameters': {
                'type': 'object',
                'properties': {
                    'input_json': {
                        'description': '含有个体年龄数据的JSON格式字符串',
                        'type': 'string'
                    }
                },
                'required': ['input_json']
            },
            'returns': {
                'description': '计算完成后的所有人年龄总和，返回结果为JSON字符串类型对象',
                'type': 'string'
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'calculate_married_count',
            'description': '从给定的JSON格式字符串中解析出DataFrame，计算所有已婚人数，并以JSON格式返回结果。',
            'parameters': {
                'type': 'object',
                'properties': {
                    'input_json': {
                        'description': '含有个体婚姻状态数据的JSON格式字符串',
                        'type': 'string'
                    }
                },
                'required': ['input_json']
            },
            'returns': {
                'description': '计算完成后的所有已婚人数，以JSON字符串类型对象返回',
                'type': 'string'
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_flight_number',
            'description': '从给定的JSON格式字符串中解析出DataFrame，根据始发地，目的地和日期查询对应的航班号，并以JSON格式返回结果。',
            'parameters': {
                'type': 'object',
                'properties': {
                    'data': {
                        'description': '出发日期',
                        'type': 'string'
                    },
                    'departure': {
                        'description': '始发地',
                        'type': 'string'
                    },
                    'destination': {
                        'description': '目的地',
                        'type': 'string'
                    }
                },
                'required': ['data', 'departure', 'destination']
            },
            'returns': {
                'description': '查询到的航班号，返回结果为JSON字符串类型对象',
                'type': 'string'
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'fetch_latest_qqemail_content',
            'description': '查询指定用户的QQ邮箱中的最后一封邮件的内容',
            'parameters': {
                'type': 'object',
                'properties': {
                    'user_email': {
                        'description': '需要查询的QQ邮箱的用户邮箱',
                        'type': 'string'
                    },
                    'user_pass': {
                        'description': '需要查询的QQ邮箱的用户码',
                        'type': 'string'
                    }
                },
                'required': ['user_email', 'user_pass']
            },
            'returns': {
                'description': '返回最后一封邮件全部信息的JSON格式字符串，如果查询失败，则返回包含错误信息的JSON格式字符串',
                'type': 'string'
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'send_email',
            'description': '借助QQ邮箱API创建并发送邮件的函数。',
            'parameters': {
                'type': 'object',
                'properties': {
                    'user_to': {
                        'description': '邮件发送的目标邮箱地址',
                        'type': 'string'
                    },
                    'subject': {
                        'description': '邮件主题',
                        'type': 'string'
                    },
                    'user_pass': {
                        'description': '邮箱授权码',
                        'type': 'string'
                    },
                    'user_from': {
                        'description': '邮件发送的源邮箱地址',
                        'type': 'string'
                    },
                    'message_text': {
                        'description': '邮件的全部内容',
                        'type': 'string'
                    }
                },
                'required': ['user_to', 'subject', 'user_pass', 'user_from', 'message_text']
            },
            'returns': {
                'description': '发送结果的字典，包含邮件ID和发送状态',
                'type': 'object'
            }
        }
    }
]


class ChatConversation:
    """
    ChatConversation 类 用于 与大模型进行聊天对话，并可选择是否使用外部功能函数。

    属性:
    - model (Str): 调用的 OpenAI 大模型名称
    - messages (List): 一个包含用户和系统消息的列表
    - function_repository (dict): 存储可选外部功能函数

    方法:
    - __init__ : 初始化 ChatConversation 类
    - add_functions : 添加外部功能函数到 ChatConversation 类
    - _call_Chat_model: 调用 OpenAI 大模型 进行聊天对话
    - run : 运行聊天会话并获取最终的对话结果(响应)
    """

    # model = "glm-4" 说明这个类的model属性默认值是"glm-4"，可以通过实例化对象的时候传入参数来修改这个值
    def __init__(self, model="glm-4"):
        """
        初始化 ChatConversation 类
        """
        # model: 调用的 OpenAI 大模型名称
        self.model = model
        # message: 一个包含用户和系统消息的列表
        self.messages = []
        # function_repository: 存储可选外部功能函数
        self.function_repository = {}

    def add_functions(self, function_list):
        """
        添加外部功能函数到 ChatConversation 类

        参数:
        - function_list (list): 一个包含多个功能函数的列表。
        """
        self.function_repository = {func.__name__: func for func in function_list}

    def _call_chat_model(self, functions=None, include_functions=False):
        """
        调用 OpenAI 大模型 进行聊天对话

        参数:
        - functions (list): 一个包含多个功能函数的列表。
        - include_functions (bool): 是否包含功能函数和自动调用功能函数

        返回:
        - dict: 包含对话的 JSON 格式
        """

        params = {
            "model": self.model,
            "messages": self.messages,
            "top_p": 0.7,
            "temperature": 0.9,
            "stream": False,
            "max_tokens": 2000
        }

        if include_functions:
            # tools 一开始并没有定义，所以这里需要定义一下
            params["tools"] = functions
        try:
            # 假设 params 是正确的
            response = client_zhipu.chat.completions.create(**params)
            return response
        except ValueError as ve:
            print(f"捕获到ValueError: {ve}")
            return None
        except TypeError as te:
            print(f"捕获到TypeError: {te}")
            return None
        except Exception as e:
            print(f"这里有一个未预料到的错误: {e}")
            return None

    def run(self, functions_list=None):
        """
        运行聊天会话并获取最终的对话结果(响应)

        参数:
        - functions_list (list): 包含功能函数的列表，当值为 None 时，默认只进行常规对话

        返回:
        str: 最终的对话结果(响应)
        """

        try:
            # 如果不传入外部功能函数列表，则只进行常规对话
            if functions_list is None:
                response = self._call_chat_model()
                final_response = response.choices[0].message.content
                return final_response
            else:
                # 添加外部功能函数到 ChatConversation 类
                self.add_functions(functions_list)
                # 如果传人了外部功能函数列表，先生成每个功能函数对应的 JSON Schema 描述
                # functions = AutoFunctionGenerator(functions_list).auto_generate()
                functions = functions_dec
                # functions =[{'type': 'function', 'function': {'name': 'calculate_total_age_function',
                # 'description': '从给定的JSON格式字符串中解析出DataFrame，计算所有人的年龄总和，并以JSON格式返回结果。', 'parameters': {'type':
                # 'object', 'properties': {'input_json': {'description': '含有个体年龄数据的JSON格式字符串', 'type': 'string'}},
                # 'required': ['input_json']}, 'returns': {'description': '计算完成后的所有人年龄总和，返回结果为JSON字符串类型对象',
                # 'type': 'string'}}}, {'type': 'function', 'function': {'name': 'calculate_married_count',
                # 'description': '从给定的JSON格式字符串中解析出DataFrame，计算所有已婚人数，并以JSON格式返回结果。', 'parameters': {'type':
                # 'object', 'properties': {'input_json': {'description': '含有个体婚姻状态数据的JSON格式字符串', 'type': 'string'}},
                # 'required': ['input_json']}, 'returns': {'description': '计算完成后的所有已婚人数，返回结果为JSON字符串类型对象',
                # 'type': 'string'}}}, {'type': 'function', 'function': {'name': 'get_flight_number', 'description':
                # '从给定的JSON格式字符串中解析出DataFrame，根据始发地，目的地和日期查询对应的航班号，并以JSON格式返回结果。', 'parameters': {'type': 'object',
                # 'properties': {'data': {'description': '出发日期', 'type': 'string'}, 'departure': {'description':
                # '始发地', 'type': 'string'}, 'destination': {'description': '目的地', 'type': 'string'}}, 'required': [
                # 'data', 'departure', 'destination']}, 'returns': {'description': '查询到的航班号，返回结果为JSON字符串类型对象',
                # 'type': 'string'}}}]

                # print("functions:", functions)

                # 模型对话分为两个阶段，第一阶段是调用 OpenAI 大模型 进行聊天对话，第二阶段是调用外部功能函数，自动调用功能函数，并将结果返回给用户
                # 第一阶段
                response = self._call_chat_model(functions, include_functions=True)
                # print('------1',response)
                response_message = response.choices[0].message
                # 打印输出查看第一阶段的response_message
                # print("response_message:", response_message)
                # 如果第一阶段的response_message中包含了tool_calls
                if response_message.tool_calls is not None:
                    # print("response_message.tool_calls[0]:", response_message.tool_calls[0])
                    # response_message.tool_calls[0]: CompletionMessageToolCall(id='call_8760198228301052175',
                    #                                                           function=Function(
                    #                                                               arguments='{"input_json":"{\\"columns\\":[\\"Name\\",\\"Age\\",\\"Salary\\",\\"IsMarried\\"],\\"index\\":[0,1,2,3,4,5],\\"data\\":[[\\"Tom\\",25,5000,true],[\\"Jerry\\",22,6000,false],[\\"Mickey\\",30,7000,true],[\\"Minnie\\",28,8000,true],[\\"Donald\\",35,9000,true],[\\"Daisy\\",33,10000,false]]}"}',
                    #                                                               name='calculate_total_age_function'),
                    #                                                           type='function', index=0)
                    # 提取函数名称
                    function_name = response_message.tool_calls[0].function.name

                    # 提取函数对象
                    function_call_exist = self.function_repository.get(function_name)
                    # 打印输出查看函数对象
                    # print(" :", function_call_exist)
                    # 打印输出查看第一阶段的response_message
                    # print("response_message:", response_message)
                    # 打印输出查看第一阶段的function_name
                    print("function_name:", function_name)
                    print("function_call_exist:", function_call_exist)
                    if not function_call_exist:
                        # 如果函数不存在，则打印错误信息
                        print(f"Function {function_name} 不在 function_repository 中")
                        return None
                    # 提取函数参数信息
                    function_args = json.loads(response_message.tool_calls[0].function.arguments)
                    # 打印输出查看函数参数信息
                    # print("function_args:", function_args)
                    # 提取函数处理后的结果
                    function_response = function_call_exist(**function_args)

                    # 做个标记，message = 原始的输入 + first_stage_response + function_response

                    # message中拼接 first_stage_response
                    self.messages.append(response_message.model_dump())

                    # message中拼接 function_response
                    self.messages.append({
                        "role": "tool",
                        "content": function_response,
                        "tool_call_id": response_message.tool_calls[0].id
                    })

                    # 第二阶段
                    second_response = self._call_chat_model(functions=functions, include_functions=True)

                    # 获取最后的对话结果
                    final_response = second_response.choices[0].message.content
                    # 打印输出查看最后的对话结果
                    # print(f"final_response_tools:{final_response}\n")
                else:
                    final_response = response_message.content
                    # 打印输出查看最后的对话结果
                    # print(f"final_response_none:{final_response}\n")
                return final_response
        except Exception as e:
            print(f"run这里有一个错误: {e}")
            return None
