"""
    Created by fre123 at 2024-10-11.
    Description: 常用函数
    Changelog: all notable changes to this file will be documented
"""

import hashlib

from urllib.parse import urlparse


def extract_domain(url: str) -> str:
    """
    提取域名名称
    Args:
        url (_type_): 目标 url

    Returns:
        _type_:  域名主体
    """
    parsed_url = urlparse(url)
    if ".com.cn" in parsed_url.netloc:
        domain = parsed_url.netloc.split(".")[-3]
    else:
        domain = parsed_url.netloc.split(".")[-2]
    return domain


def md5_encryption(string: str) -> str:
    """
    对字符串进行md5加密
    Args:
        string (str): 加密目标字符串

    Returns:
        str: 加密后字符串
    """
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return m.hexdigest()


def read_file(file_path: str) -> list:
    """
    读取文本内容
    Args:
        file_path (str): 文件路径
    Returns:
        list: 每行文件内容组成的列表
    """
    try:
        with open(file_path, encoding="utf-8") as fp:
            file_list = [_.strip() for _ in fp.readlines()]
    except Exception as _:
        file_list = []
    return file_list
