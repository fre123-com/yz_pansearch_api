"""
Created by fre123 at 2024-10-11.
Description: Flask 蓝图
Changelog: all notable changes to this file will be documented
"""

from flask import Blueprint

from src.views.v1.ping import ping
from src.views.v1.search import get_dj_3v, get_kk, get_pansearch, get_xxq, get_soushuju, get_star
from src.views.v1.tools.proxy import proxy

bp_api = Blueprint("bp_api", __name__)
version = "/v1"

bp_api.add_url_rule(f"{version}/ping", view_func=ping, methods=["GET"])
bp_api.add_url_rule(f"{version}/search/get_kk", view_func=get_kk, methods=["POST"])
bp_api.add_url_rule(f"{version}/search/get_dj", view_func=get_dj_3v, methods=["POST"])
bp_api.add_url_rule(
    f"{version}/search/get_pansearch", view_func=get_pansearch, methods=["POST"]
)
bp_api.add_url_rule(f"{version}/search/get_xxq", view_func=get_xxq, methods=["POST"])
bp_api.add_url_rule(
    f"{version}/search/get_soushuju", view_func=get_soushuju, methods=["POST"]
)
bp_api.add_url_rule(f"{version}/search/get_star", view_func=get_star, methods=["POST"])
bp_api.add_url_rule(
    f"{version}/tools/proxy",
    view_func=proxy,
    methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
)
