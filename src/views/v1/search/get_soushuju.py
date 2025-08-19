"""
Created by kxy at 2025-07-25.
Description: 获取 soushuju 资源接口
Changelog: all notable changes to this file will be documented
"""

from flask import current_app, request

from src.collector import soushuju_spider
from src.common import ResponseField, UniResponse, response_handle, token_required
from src.config import LOGGER, Config
from src.logic.cache_tools import get_cache, set_cache
from src.logic.pan_quark_tools import get_quark_url_by_txt, get_share_url_token
from src.utils import md5_encryption


@token_required()
def get_soushuju():
    """
    测试接口
    """
    app_logger: LOGGER = current_app.config["app_logger"]
    app_config: Config = current_app.config["app_config"]
    # 从 req header 头获取 PROXY_MODEL
    proxy_model = request.headers.get("PROXY-MODEL", 0)
    # 默认开启缓存
    is_cache = request.headers.get("IS-CACHE", "1")
    # 默认提取夸克链接
    pan_type = request.headers.get("PAN-TYPE", "quark")
    check_pan_url = request.headers.get("CHECK-PAN-URL", "0")
    pan_type_list = pan_type.lower().strip().split(";")

    # 获取请求数据
    post_data: dict = request.json
    kw = post_data.get("kw")

    if kw:
        # 缓存处理
        md5_key = md5_encryption(f"{kw}_{proxy_model}")
        cache_key = f"yz_pansearch:soushuju:{md5_key}"
        redis_data = None
        if is_cache == "1":
            redis_data = get_cache(cache_key)
        if redis_data:
            result = redis_data
        else:
            spider_data = soushuju_spider.run_spider(kw, proxy_model)
            target_data = []

            if spider_data:
                for res in spider_data:
                    res_dict = {}
                    for each_pan_type in pan_type_list:
                        res_url_str = res.get("url", "")
                        if each_pan_type == "quark":
                            quark_url_list = get_quark_url_by_txt(res_url_str)
                            c_quark_url_list = []
                            if check_pan_url == "1":
                                for each_pan_url in quark_url_list:
                                    quark_url_check_resp = get_share_url_token(
                                        quark_url=each_pan_url["url"]
                                    )
                                    if quark_url_check_resp.get("is_valid"):
                                        c_quark_url_list.append(each_pan_url)
                            else:
                                c_quark_url_list = quark_url_list
                            if c_quark_url_list:
                                res_dict[each_pan_type] = c_quark_url_list
                        elif each_pan_type == "baidu":
                            code = res.get("code", "")
                            res_dict[each_pan_type] = {"url": res_url_str, "code": code}
                        else:
                            pass
                    if res_dict:
                        target_data.append(
                            {
                                "title": res.get("title", kw) or kw,
                                "description": "",
                                "res_dict": res_dict,
                            }
                        )
            else:
                # 数据抓取失败
                app_logger.error(f"数据抓取失败( soushuju 源，请考虑使用代理)，kw: {kw}")

            result = {
                **UniResponse.SUCCESS,
                **{
                    ResponseField.DATA: {
                        "total": len(target_data),
                        "rows": target_data,
                    }
                },
            }
            if target_data and is_cache == "1":
                set_cache(cache_key, result, expire=app_config.CACHE_TTL)
    else:
        result = UniResponse.PARAM_ERR
    return response_handle(request=request, dict_value=result)
