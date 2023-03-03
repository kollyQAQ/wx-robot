import json
import requests


def chat(keyword):
    url = "https://api.openai.com/v1/chat/completions"

    header = {
        "Authorization": "Bearer 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",
        'content-type': 'application/json',
    }

    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": keyword}],
    }

    try:
        res = requests.post(url, data=json.dumps(body), headers=header)
        res.encoding = 'utf-8'
    except BaseException:
        return "接口异常"

    if res.status_code != 200:
        return "接口异常"

    return res.json()['choices'][0]['message']['content']


if __name__ == "__main__":
    a = "@小糖同学 写的不够详细"
    a = a[6:]
    # print(chat("你是谁？"))
    print(a)
