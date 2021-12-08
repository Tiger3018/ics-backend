# with Oauth session in authserver.cqu.edu.cn, access my.cqu.edu.cn without password

# local import
from login import requests, logging, parse, login, headers
from typing import Union
import os, time

login_page_url = "http://authserver.cqu.edu.cn/authserver/login"
service_name_brief = "tt"
service_name = "timetable-prod"
service_url_suffix = "/" + service_name_brief + "/token-index"
service_url_prefix = "https://my.cqu.edu.cn"
service_url_prefix_fallback = "http://my.cqu.edu.cn"

def loginOauth(cas_token: str) -> Union[requests.Session, None]:

    logger = logging.getLogger(__name__)
    session = requests.Session()

    # step1: 获取登录页面
    logger.info("正在提交 TGT")
    resp = session.get(
        url=login_page_url,
        params={
            "service": service_url_prefix_fallback + "/authserver/authentication/cas"
        },
        headers=headers,
        cookies={
            "CASTGC": cas_token,
            "JSESSIONID": _ if (_ := os.getenv("JSID")) else ""
            },
        allow_redirects=False
    )
    if resp.status_code != 302:
        logger.error("登录页面跳转失败")
        return None

    # step3: 进入目标服务
    logger.info("正在利用 CASTGC 与选课网对接")
    # omit the redirection: http -> https
    target_url = resp.headers["Location"].replace("http", "https")
    resp = session.get(
        url=target_url,
        headers=headers,
        allow_redirects=False
    )
    logger.debug(resp.status_code, resp.headers, target_url)
    if resp.status_code not in (200, 302):
        logger.error("ticket传送失败")
        return None

    # step4: 获取oauth token
    logger.info("正在进行OAuth认证")
    oauth_url = service_url_prefix + "/authserver/oauth/authorize"
    resp = session.get(
        url=oauth_url,
        params={
            "client_id": service_name,
            "response_type": "code",
            "scope": "all",
            "state": "",
            "redirect_uri": service_url_prefix + service_url_suffix
        },
        headers=headers,
        allow_redirects=False
    )
    logger.debug(resp.status_code, resp.headers)
    if resp.status_code != 302:
        logger.error("OAuth 认证 | Authorize 失败")
        return None

    # step5: 生成oauth验证表单并提交验证，模拟token-index
    # 从Location中取出code
    params = parse.parse_qs(parse.urlparse(resp.headers["Location"]).query)
    oauth_formdata = {
        "client_id": service_name,
        "client_secret": "app-a-1234",
        "code": params["code"][0],
        "redirect_uri": service_url_prefix + service_url_suffix,
        "grant_type": "authorization_code"
    }
    # 加入Basic验证, 值为client_id:client_secret的base64编码
    headers["Authorization"] = "Basic dGltZXRhYmxlLXByb2Q6YXBwLWEtMTIzNA=="
    oauth_url = service_url_prefix + "/authserver/oauth/token"
    resp = session.post(
        url=oauth_url,
        headers=headers,
        data=oauth_formdata
    )
    logger.debug(resp.status_code, resp.headers)
    if resp.status_code != 200:
        logger.error("OAuth 认证 | access_token 失败")
        return None
    headers["Authorization"] = "Bearer " + resp.json()["access_token"]
    logger.info("登录成功")
    return session
