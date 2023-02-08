import requests

def chat_with_gpt3(message):
    # 设置OpenAI的API密钥
    API_KEY = "你的API密钥"

    # 设置OpenAI API的端点
    endpoint = "https://api.openai.com/v1/engines/davinci/jobs"

    # 设置API调用的参数
    params = {
        "text": message,
        "model": "davinci",
        "temperature": 0.5,
        "max_tokens": 200,
    }

    # 设置API调用的标头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    # 发送API请求
    response = requests.post(endpoint, json=params, headers=headers)

    # 检查响应的状态码
    if response.status_code != 200:
        raise Exception("无法向OpenAI API发送请求")

    # 提取响应文本
    response_text = response.json()["choices"][0]["text"]

    # 将响应文本发送到飞书
    # 发送消息到飞书的代码在此处
    print(response_text)

# 示例用法
chat_with_gpt3("你好，今天怎么样？")

