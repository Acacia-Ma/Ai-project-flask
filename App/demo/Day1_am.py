import json

import pandas as pd
from openai import OpenAI
from zhipuai import ZhipuAI
from io import StringIO

# 创建一个简单的DataFrame
df_complex = pd.DataFrame({
    'Name': ['张三', '李四', '王五'],
    'Age': [25, 30, 35],
    'Salary': [50000.0, 100000.5, 150000.75],
    'IsMarried': [True, False, True]
})

print(df_complex)

# 方法一，使用openai库
client = OpenAI(
    api_key="dae4b7d3a476814fa8938ee5183045af.9UDOI9jvUOcpkHx2",  # 你自己的api key
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)
# client = OpenAI(
#     api_key="dae4b7d3a476814fa8938ee5183045af.9UDOI9jvUOcpkHx2",  # 你自己的api key
#     base_url="http://10.203.81.196:41739/v1/"
# )


def zhipu_api_open(messages: list):
    """为提供的对话消息创建新的回答
    Args:
    messages (list): 完整的对话消息
    """
    completion = client.chat.completions.create(model="glm-4", messages=messages)
    print(completion.choices[0].message.content)


# 方法二：使用本家自带的库
client_zhipu = ZhipuAI(api_key="dae4b7d3a476814fa8938ee5183045af.9UDOI9jvUOcpkHx2")  # 你自己的api key
# messages = []
# messages = [{"role": "system", "content": "你是一位优秀的数据分析师，现在有这样一份数据集：'%s'" % df_complex},
#             {"role": "user", "content": "请解释一下这个数据集的分布情况"}]

# response = client.chat.completions.create(
#     model="glm-4",  # 填写需要调用的模型名称
#     messages=messages,
# )
# 使用大模型看是否可以解读数据集
# print(response.choices[0].message)
# messages.append(response.choices[0].message.model_dump())

# 将DataFrame转换为JSON格式,orient='split'参数将数据、索引和列分开存储
df_complex_json = df_complex.to_json(orient='split')
print(df_complex_json)


# 编写计算年龄总和的函数
def calculate_total_age_from_split_json(input_json):
    """
    从给定的JSON格式字符串（按'split'方向排列）中解析出DataFrame，计算所有人的年龄总和，并以
    JSON格式返回结果。
    参数:
    input_json (str): 包含个体数据的JSON格式字符串。
    返回:
    str: 所有人的年龄总和，以JSON格式返回。
    """
    # 将JSON字符串转换为DataFrame
    df = pd.read_json(StringIO(input_json), orient='split')
    # 计算年龄总和
    total_age = df['Age'].sum()
    # 将结果转换为字符串形式，然后使用json.dumps()转换为JSON格式,导入json模块 语句：import json
    return json.dumps({"total_age": str(total_age)})


# 使用函数计算年龄总和，并以JSON格式输出
result = calculate_total_age_from_split_json(df_complex_json)
print("The JSON output is:", result)

# 定义函数仓库,将函数注册到函数仓库中
'''
函数库对象必须是一个字典，一个键值对代表一个函数，其中key是代表函数名称的字符串，而value表
示对象的函数。所以上述过程可以简单的理解为：所谓的外部函数库，就是用一个大的字典来存储某应
用场景中的所需要的所有函数定义。
'''
function_repository = {
    "calculate_total_age_from_split_json": calculate_total_age_from_split_json,
}
# 构建外部函数的JSON Schema数据
calculate_total_age_describe = {
    "type": "function",
    "function": {
        "name": "calculate_total_age_from_split_json",
        "description": "计算年龄总和的函数，从给定的JSON格式字符串（按'split'方向排列）中"
                       "解析出DataFrame，计算所有人的年龄总和，并以JSON格式返回结果。",
        "parameters": {
            "type": "object",
            "properties": {
                "input_json": {
                    "type": "string",
                    "description": "执行计算年龄总和的数据集"},
            },
            "required": ["input_json"],
        },
    }
}
# 创建函数列表
tools = [calculate_total_age_describe]

# 定义消息列表
messages = [
    {
        "role": "system",
        "content": "你是一位优秀的数据分析师, 现在有这样一个数据集\ninput_json：%s，数据集以JSON形式呈现" % df_complex_json
    },
    {
        "role": "user",
        "content": "请在数据集input_json上执行计算所有人年龄总和函数"
    }
]


def zhipu_api(messages: list):
    """为提供的对话消息创建新的回答
    Args:
        messages (list): 完整的对话消息
    """
    print(tools)
    # 向模型提问
    response = client_zhipu.chat.completions.create(
        model="glm-4",
        messages=messages,
        top_p=0.7,
        temperature=0.9,
        stream=False,
        max_tokens=2000,
        tools=tools,
        # 可以不设置
        tool_choice="auto",
    )
    print(response.choices[0].message.content)
    # 保存交互过程中的关键信息
    # 保存交互过程中的函数名称
    function_name = response.choices[0].message.tool_calls[0].function.name
    # 加载交互过程中的参数
    function_args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    # 保存具体的函数对象
    local_fuction_call = function_repository[function_name]
    # 完成模型计算
    final_response = local_fuction_call(**function_args)
    print("final_response:", final_response)
    # 在messages中追加外部函数返回的结果
    messages.append({
        "role": "tool",
        "content": final_response,
        "tool_call_id": response.choices[0].message.tool_calls[0].id
    })
    # 再次向模型提问
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=messages,
        tools=tools,
    )
    # 将结果追加到messages中
    messages.append(response.choices[0].message.model_dump())


# 调用函数
if __name__ == '__main__':
    messages = [
        {
            "role": "system",
            "content": "你是一位优秀的数据分析师, 现在有这样一个数据集\ninput_json：%s，数据集以JSON形式呈现" % df_complex_json
        },
        {
            "role": "user",
            "content": "请在数据集input_json上执行计算所有人年龄总和函数"
        }
    ]
    zhipu_api_open(messages)
    zhipu_api(messages)
