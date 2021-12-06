# with Oauth session in authserver.cqu.edu.cn, access my.cqu.edu.cn without password

# local import
from login import requests, logging, parse, login, headers
from typing import Union
import os

login_page_url = "http://authserver.cqu.edu.cn/authserver/login"
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
    # target_url = target_prefix + "?ticket=" + cas_token
    while True:
        target_url = resp.headers["Location"]
        resp = session.get(
            url=target_url,
            headers=headers,
            allow_redirects=False
        )
        if resp.status_code == 302:
            break # ->my.cqu.edu.cn
        elif resp.status_code == 301:
            continue # http -> https, refer to 2e4bebc:login_auth.py#19,
            # authserver only accept http://my domain. What's more, any service under https://my will fallback to http://my when request a login,
            # e.g. curl https://my.cqu.edu.cn/sms/ -v -> [200] "... href='...service=http%3A%2F%2Fmy.cqu.edu.cn%2Fsms%2F' ..."
        else:
            logger.error("重定向失败")
            return None

    # step4: 获取oauth token
    logger.info("正在进行OAuth认证")
    oauth_url = service_url_prefix + "/authserver/oauth/authorize"
    resp = session.get(
        url=oauth_url,
        params={
            "client_id": "enroll-prod",
            "response_type": "code",
            "scope": "all",
            "state": "",
            "redirect_uri": service_url_prefix + "/enroll/token-index"
        },
        headers=headers,
        allow_redirects=False
    )
    if resp.status_code != 302:
        logger.error("OAuth认证失败")
        return None

    # step5: 生成oauth验证表单并提交验证
    # 从Location中取出code
    params = parse.parse_qs(parse.urlparse(resp.headers["Location"]).query)
    oauth_formdata = {
        "client_id": "enroll-prod",
        "client_secret": "app-a-1234",
        "code": params["code"][0],
        "redirect_uri": service_url_prefix + "/enroll/token-index",
        "grant_type": "authorization_code"
    }
    # 加入Basic验证, 值为client_secret的base64编码, 这里写死
    headers["Authorization"] = "Basic ZW5yb2xsLXByb2Q6YXBwLWEtMTIzNA=="
    oauth_url = service_url_prefix + "/authserver/oauth/token"
    resp = session.post(
        url=oauth_url,
        headers=headers,
        data=oauth_formdata
    )
    if resp.status_code != 200:
        logger.error("OAuth认证失败")
        return None
    headers["Authorization"] = "Bearer " + resp.json()["access_token"]
    logger.info("登录成功")
    return session
