# 首先导入必要的模块
import requests
import json

# 设置飞书机器人请求的 URL
url = "https://openapi.feishu.cn/open-apis/bot/v1/message/send"

# 设置请求头，指定内容类型为 json
headers = {
    "Content-Type": "application/json"
}

# 设置飞书机器人的 Access Token
# 如果您没有飞书机器人，可以在飞书开放平台上申请一个
access_token = "YOUR_ACCESS_TOKEN"

# 设置请求体
# 注意：要将 access_token 字段加入请求头
data = {
    "msg_type": "text",
    "content": {
        "text": "你好，这是一条飞书机器人发送的消息。"
    },
    "to_all": True
}

# 发送请求，指定请求方法为 post
response = requests.post(url, headers=headers, data=json.dumps(data), access_token=access_token)

# 打印响应结果
print(response.text)

