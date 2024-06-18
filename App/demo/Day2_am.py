from zhipuai import ZhipuAI

client_zhipu = ZhipuAI(api_key="dae4b7d3a476814fa8938ee5183045af.9UDOI9jvUOcpkHx2")  # 你自己的api key
from autofunctiongenerator import AutoFunctionGenerator
import json
import pandas as pd
from functionsList import calculate_total_age_function, calculate_married_count, get_flight_number


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
                functions = AutoFunctionGenerator(functions_list).auto_generate()

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


def chat_with_assistant(functions_list=None,
                        prompt="你好!",
                        model="glm-4",
                        system_message="我是你的私人小助理"):
    # 创建 ChatConversation 类的实例
    chat_conversation = ChatConversation(model=model)

    # 添加系统信息和用户输入 到 messages 列表中
    messages = [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    chat_conversation.messages = messages

    while True:
        # 调用run方法处理对话，并获取最终的对话结果(响应)
        response = chat_conversation.run(functions_list=functions_list)
        # 打印输出查看最终的对话结果(响应)
        print(f"模型响应: {response}\n")
        # 添加模型回答到 messages 列表中
        messages.append({"role": "assistant", "content": response})

        # 询问用户是否继续对话
        user_input = input("是否继续对话？(yes/no): ")

        # 如果用户输入 no，则退出对话
        if user_input.lower() == "no":
            break

        # 添加用户输入到 messages 列表中
        messages.append({"role": "user", "content": user_input})
        # 更新 ChatConversation 类的 messages 属性
        chat_conversation.messages = messages


# 测试 ChatConversation 类
df_complex = pd.DataFrame({
    "Name": ["Tom", "Jerry", "Mickey", "Minnie", "Donald", "Daisy"],
    "Age": [25, 22, 30, 28, 35, 33],
    "Salary": [5000, 6000, 7000, 8000, 9000, 10000],
    "IsMarried": [True, False, True, True, True, False]
})

df_complex_string = df_complex.to_string()
# 将 DataFrame 转换为 JSON 格式字符串,orient='split'表示 参数将数据、索引和列标签作为列表返回
df_complex_json = df_complex.to_json(orient='split')
functions_list = [calculate_total_age_function, calculate_married_count, get_flight_number]

if __name__ == "__main__":
    # 创建 ChatConversation 类的实例
    chat_conversation = ChatConversation()

    chat_conversation.messages = [
        {
            "role": "system",
            "content": "你是一位优秀的数据分析师, 现在有这样一个数据集\ninput_json：%s，数据集以JSON形式呈现" % df_complex_json
        },
        {
            "role": "user",
            "content": "请在数据集input_json上执行计算所有人年龄总和函数"
        }
    ]
    # 调用run方法处理对话，并获取最终的对话结果(响应)
    # response = chat_conversation.run(functions_list=functions_list)
    # # 打印输出查看最终的对话结果(响应)
    # print(f"模型响应: {response}\n")

    # chat_with_assistant 函数用于与助手进行对话
    chat_with_assistant(functions_list=functions_list)
