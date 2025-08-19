"""
Created by kxy at 2025-07-25.
Description: https://sou.s.sou.soushuju.cn/search=keywo 爬虫脚本
    pipenv run python src/collector/ssoushuju_spider.py
Changelog: all notable changes to this file will be documented
"""

import re
import urllib.parse

from lxml import html

from src.collector import REQ_SESSION, data_config
from src.config import LOGGER


def fetch_page_data(url, headers, proxy: None):
    """发送 GET 请求并解析网页内容"""
    try:
        response = REQ_SESSION.get(url, headers=headers, timeout=5, proxies=proxy)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return {"err_msg": str(e)}


def parse_page_data(kw, html_content):
    """使用 lxml 解析网页内容并提取所需数据"""
    tree = html.fromstring(html_content)
    data_list = []
    items = tree.xpath('//div[@class="box"]//div[@class="info"]')

    for item in items:
        title = (
            item.xpath("text()[1]")[0].split("\n")[1].strip()
            if item.xpath("text()[1]")
            else ""
        )

        url = item.xpath(".//a/@href")[0] if item.xpath(".//a/@href") else ""

        code = (
            re.search(r"提取码[:：]\s*(\w{4})", item.text_content()).group(1)
            if re.search(r"提取码[:：]\s*(\w{4})", item.text_content())
            else ""
        )
        if code == "无需密码":
            code = ""

        data_list.append({"title": title, "url": url, "code": code})

    return data_list


def run_spider(kw: str, proxy_model: int = 0):
    """启动爬虫并返回数据"""
    # 将字符串转换为 URL 编码
    encoded_kw = urllib.parse.quote(kw)
    req_url = f"https://sou.s.sou.soushuju.cn/?search={kw}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": f"https://www.pansearch.me/search?keyword={encoded_kw}",
        "Content-Type": "text/html",
        **data_config.SPIDER_CONFIG["REQUEST_HEADERS"],
    }

    if proxy_model:
        proxy = {
            "http": data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_URL"],
            "https": data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_URL"],
        }
        headers.update(
            data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_HEADERS"]
        )
        LOGGER.info("Pansearch Spider 使用代理获取数据")
    else:
        proxy = {}

    html_content = fetch_page_data(req_url, headers, proxy)
    if isinstance(html_content, dict) and "err_msg" in html_content:
        LOGGER.error(f"请求失败: {html_content['err_msg']}")
        return None

    parsed_data = parse_page_data(kw, html_content)
    return parsed_data


if __name__ == "__main__":
    from pprint import pprint

    data = run_spider(kw="奥特曼", proxy_model=0)
    if data:
        pprint(data)
