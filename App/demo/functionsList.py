# 定义消息列表
import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from io import StringIO

import pandas as pd

# 定义函数
def calculate_total_age_function(input_json):
    """
    从给定的JSON格式字符串（按'split'方向排列）中解析出DataFrame，计算所有人的年龄总和，并以JSON格式返回结果。
    参数:
    input_json(str): 含有个体年龄数据的JSON格式字符串
    返回:
    str: 计算完成后的所有人年龄总和，返回结果为JSON字符串类型对象
    """

    # 将JSON字符串转换为DataFrame
    df = pd.read_json(StringIO(input_json), orient='split')
    # 计算年龄总和
    total_age = df['Age'].sum()
    # 将结果转换为字符串形式，然后使用json.dumps()转换为JSON格式,导入json模块 语句：import json
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
    df = pd.read_json(StringIO(input_json), orient='split')
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

def send_email(user_from,user_pass,user_to,subject,message_text):
    """
    借助QQ邮箱 API创建并发送邮件函数
    :param user_to: 必要参数，字符串类型，用于表示邮件发送的目标邮箱地址；
    :param subject: 必要参数，字符串类型，用于表示邮件主题；
    :param user_pass: 必要参数，字符串类型，用于表示邮箱授权码；
    :param user_from: 必要参数，字符串类型，用于表示邮件发送的源邮箱地址；
    :param message_text: 必要参数，字符串类型，用于表示邮件全部中文；
    :return: 返回发送结果字典，若发送成功，则返回包含邮件ID和发送状态的字典。
    """

    # 邮件内容
    subject = subject
    body = message_text

    # 构建邮件
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = user_from
    msg['To'] = user_to

    # 发送邮件
    smtp_server = 'smtp.qq.com'
    smtp_port = 587
    sender_email = user_from
    password = user_pass
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, [msg['To']], msg.as_string())
        print('邮件发送成功')
        return json.dumps({'status': 'success'})
    except Exception as e:
        print('邮件发送失败')
        return json.dumps({'status': 'failed'})