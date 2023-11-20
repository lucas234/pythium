# -*- coding: UTF-8 -*-
# @Project: gls_automation_python
# @File: base_session
# @Author：Lucas Liu
# @Time: 2021/10/8 1:24 下午
# @Software: PyCharm
from requests import Session, Response
import allure
import os
import json
from functools import partial
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import urljoin, urlparse
from loguru import logger


class HttpSession(Session):
    PROXIES = {"http": "", "https": ""}
    TIMEOUT = 10

    def __init__(self, base_url=None):
        self.base_url = base_url
        super(HttpSession, self).__init__()
        self.hooks["response"] = [self._logging_hook]
        # set proxy
        # self._set_proxy(self.PROXIES)
        # set default timeout
        self.request = partial(self.request, timeout=self.TIMEOUT)
        # adapter = self._retry_adapter()
        # self.mount('http://', adapter)
        # self.mount('https://', adapter)

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.base_url, url)
        return super(HttpSession, self).request(method, url, *args, **kwargs)

    def _set_proxy(self, proxies):
        self.proxies.update(proxies)

    @staticmethod
    def _retry_adapter():
        """
        sleep N seconds after failed
        expression: {backoff factor} * (2 ** ({number of total retries} - 1))
        1 second the successive sleeps will be: 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256.
        2 seconds - 1, 2, 4, 8, 16, 32, 64, 128, 256, 512.
        """
        retry_strategy = Retry(
            total=3,
            status_forcelist=[401, 404, 429, 500, 501, 502, 503, 504],
            method_whitelist=frozenset(['GET', 'POST']),
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        # self.mount('http://', adapter)
        # self.mount('https://', adapter)
        return adapter

    @staticmethod
    def _logging_hook(response: Response, *args, **kwargs):
        is_log = True if os.environ.get('LOG', 'false').lower() == 'true' else False
        # if response.ok and not is_log: # only print log(not success request)
        if not is_log:
            return
        try:
            # request
            if isinstance(response.request.body, str):
                request_body = response.request.body
            else:
                request_body = json.loads(response.request.body.decode('utf-8')) if response.request.body else {}
            request_headers = response.request.headers.__dict__
            # request_headers.pop('_store')
            request_msg = f"\n< ### Request Info ###\n" \
                          f"< {response.request.method} {response.request.url}\n" \
                          f"< headers: {json.dumps(request_headers, indent=4, sort_keys=True)}\n" \
                          f"< body: {json.dumps(request_body, indent=4, sort_keys=True, ensure_ascii=False)}\n"
            logger.info(request_msg)
            allure.attach(request_msg, name=f"Request info--{urlparse(response.request.url).path}",
                          attachment_type=allure.attachment_type.JSON)
            # response
            try:
                response_body = json.dumps(response.json(), indent=4, sort_keys=True, ensure_ascii=False)
            except ValueError:
                response_body = response.text
            response_msg = f"\n> ### Response Info ###\n" \
                           f"> status_code: {response.status_code}\n" \
                           f"> duration: {response.elapsed.seconds}s\n"\
                           f"> text: {response_body}\n"
            logger.info(response_msg)
            allure.attach(response_msg, name=f"Response info--{urlparse(response.request.url).path}",
                          attachment_type=allure.attachment_type.JSON)
        except Exception as e:
            logger.info(f"logging hook error: {e}")


