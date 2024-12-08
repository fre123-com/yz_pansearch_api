"""
    Created by lrh at 2024-12-05.
    Description: https://dj.3v.hk/api/ 抓取数据
    Changelog: all notable changes to this file will be documented
"""

from src.collector import REQ_SESSION, data_config
from src.common.remote import send_get_request
from src.config import LOGGER


def get_dj2_data(kw: str, proxy_model: int = 0) -> str:
    """
    获取token
    """
    LOGGER.info(f"DJ2 Spider 请求 3v.hk 资源通道，kw:{kw}是否使用代理：{proxy_model}")
    headers = {
        **data_config.SPIDER_CONFIG["REQUEST_HEADERS"],
        **{"Content-Type": "application/json"},
    }
    if proxy_model:
        proxy = {
            "http": data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_URL"],
            "https": data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_URL"],
        }
        headers.update(
            data_config.SPIDER_CONFIG["SPIDER_PROXY_CONFIG"]["PROXY_HEADERS"]
        )
    else:
        proxy = {}
    resp = send_get_request(
        url=f"https://dj.3v.hk/api/?search={kw}",
        headers=headers,
        req_session=REQ_SESSION,
        timeout=10,
        proxies=proxy,
    )
    get_res = resp["resp_data"]
    if resp["resp_status"]:
        if get_res["msg"] is True:
            resp_data = get_res["data"]
        else:
            resp_data = []
    else:
        resp_data = []
    return resp_data


if __name__ == "__main__":
    from pprint import pprint

    res = get_dj2_data(kw="两相思", proxy_model=0)
    pprint(res)
