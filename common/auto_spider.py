import requests, json
from dao import zh_config_dao
from wxpy import *

logger = logging.getLogger('wx')

# 调知乎 api 查询今日阅读数据
def get_article_draft_by_page(cookie, offset, limit):
    url = "https://www.zhihu.com/api/v4/articles/my_drafts?offset={}&limit={}&include=data%5B*%5D.schedule".format(
        offset, limit)

    header = {
        "cookie": cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

    try:
        res = requests.get(url, headers=header)
        res.encoding = 'utf-8'
    except BaseException:
        return "接口异常"

    if res.status_code != 200:
        logger.info(res.text)
        return "接口异常"

    return res

# 调京粉 api 查询pop order
def get_article_draft_all(cookie):
    offset = 0
    limit = 10

    list = []
    isEnd = False
    while (not isEnd):
        pageRet = get_article_draft_by_page(cookie, offset, limit)
        if pageRet == "接口异常":
            isEnd = True
        else:
            json = pageRet.json()
            list.extend(json['data'])
            isEnd = json['paging']['is_end']
            offset += 10

    return list


def get_article_draft_html(aid, cookie):
    url = "https://zhuanlan.zhihu.com/api/articles/{}/draft".format(aid)

    header = {
        "cookie": cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

    try:
        res = requests.get(url, headers=header)
        res.encoding = 'utf-8'
    except BaseException:
        return "接口异常"

    if res.status_code != 200:
        logger.info(res.text)
        return "接口异常"

    return res.json()


def get_question_draft_html(qid, cookie):
    url = "https://www.zhihu.com/api/v4/questions/{}/draft?include=question%2Cschedule".format(qid)

    header = {
        "cookie": cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

    try:
        res = requests.get(url, headers=header)
        res.encoding = 'utf-8'
    except BaseException:
        return "接口异常"

    if res.status_code != 200:
        logger.info(res.text)
        return "接口异常"

    return res.json()


def post_question_draft(qid, content, cookie):
    url = "https://www.zhihu.com/api/v4/questions/{}/draft".format(qid)

    header = {
        "cookie": cookie,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'referer': "https://www.zhihu.com/question/{}/?write".format(qid),
        'content-type': 'application/json',
    }

    body = {
        "content": content,
        "delta_time": 3,
        "draft_type": "normal",
    }

    try:
        res = requests.post(url, data=json.dumps(body), headers=header)
        res.encoding = 'utf-8'
    except BaseException:
        return "接口异常"

    if res.status_code != 200:
        logger.info(res.text)
        return "接口异常"

    logger.info("保存回答草稿成功，qid:{}".format(qid))

    return res.json()


if __name__ == "__main__":
    cookie = zh_config_dao.query_config('dxck').value
    # for i in get_article_draft_all(cookie):
    #     print(i['title'], '-', i['id'])
    # print(get_article_draft_html(1651370266, cookie))
    print(get_question_draft_html(50577677, cookie))