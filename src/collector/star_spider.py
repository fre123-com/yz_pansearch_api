"""
Created by kxy at 2025-08-07.
Description: https://1.star2.cn/search/?keyword 爬虫脚本
    pipenv run python src/collector/star_spider.py
Changelog: all notable changes to this file will be documented
"""

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

def parse_page_data(html_content):
    """使用 lxml 解析网页内容并提取所需数据"""
    tree = html.fromstring(html_content)
    title = tree.xpath('.//h1')
    if not title:
        return None
    title = title[0].text.strip()
    urls = tree.xpath('.//a[@class="dlipp-dl-btn j-wbdlbtn-dlipp"]/@href')
    url = " ".join(urls) if urls else ""
    data = {"title": title, "description": "", "url": url}

    return data



def get_total_url(req_url, headers, proxy, html_content):
    """获取所有地址"""
    tree = html.fromstring(html_content)
    page = tree.xpath('.//div[@class="pagination"]/a[@class="page-item page-link hidden-sm"]/@href')[1].split("page=")
    page = int(page[1]) if len(page) == 2 else 1
    total_urls = []
    for pa in range(1,page + 1):
        page_url = f"{req_url}&page={pa}"
        page_content = fetch_page_data(page_url, headers, proxy)
        if isinstance(page_content, dict) and "err_msg" in page_content:
            LOGGER.error(f"请求失败: {page_content['err_msg']}")
            continue
        tree = html.fromstring(page_content)
        items = tree.xpath('.//ul[@class="erx-list"]/li//div[@class="a"]/a/@href')
        for it in items:
            total_urls.append(f"https://1.star2.cn{it}")
    return total_urls

def run_spider(kw: str, proxy_model: int = 0):
    """启动爬虫并返回数据"""
    # 将字符串转换为 URL 编码
    encoded_kw = urllib.parse.quote(kw)
    req_url = f"https://1.star2.cn/search/?keyword={kw}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": f"https://1.star2.cn/search/?keyword={encoded_kw}",
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

    all_data = []
    total_url = get_total_url(req_url, headers, proxy, html_content)
    for url in total_url:
        page_content = fetch_page_data(url, headers, proxy)
        if isinstance(page_content, dict) and "err_msg" in page_content:
            LOGGER.error(f"请求失败: {page_content['err_msg']}")
            continue
        page_data = parse_page_data(page_content)
        all_data.append(page_data)

    return all_data


if __name__ == "__main__":
    from pprint import pprint

    data = run_spider(kw="奥特", proxy_model=0)
    if data:
        pprint(data)
