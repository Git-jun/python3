import openai

# 初始化API Key
#openai.api_key = "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"
openai.api_key = "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"

'''
替换your_api_key为你的API密钥。
'''

def chatgpt_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

# 获取ChatGPT回复
response = chatgpt_response('python写一个飞书交互机器人')
print(response)


