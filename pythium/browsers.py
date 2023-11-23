# -*- coding: UTF-8 -*-
# @Project: pythium
# @File: _browser
# @Author：Lucas Liu
# @Time: 2022/10/14 5:21 PM
# @Software: PyCharm
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager
from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver
from pythium.emoji import Emoji
from loguru import logger


class Browsers(object):

    @staticmethod
    def _get_driver_path(browser, execute_path=None):
        """
        利用 webdriver_manager 自动下载匹配版本的浏览器driver
        地址：https://github.com/SergeyPirogov/webdriver_manager
        :param browser: 浏览器类型 chrome、firefox、ie、edge、opera
        :return: 下载的driver绝对地址
        """
        if execute_path:
            return execute_path
        # chromium_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        browser_paths = {
            "chrome": lambda: ChromeDriverManager(),
            "firefox": lambda: GeckoDriverManager(),
            "ie": lambda: IEDriverManager(),
            "edge": lambda: EdgeChromiumDriverManager(),
            "opera": lambda: OperaDriverManager(),
        }
        if browser not in browser_paths.keys():
            raise Exception(f"{Emoji.EXCEPTION} Only support the following browsers: {list(browser_paths.keys())}!")
        return browser_paths.get(browser.lower())().install()

    @staticmethod
    def remote(browser='chrome', **kwargs):
        """
        need override
        first, start server: java -jar selenium-server-standalone-4.1.2.jar standalone --host 127.0.0.1
        :return:
        """
        dc = {"browserName": browser}
        remote_driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                         # desired_capabilities=DesiredCapabilities.CHROME,
                                         desired_capabilities=dc, **kwargs)
        return remote_driver

    @classmethod
    def chrome(cls, headless=False, execute_path=None, options: ChromeOptions = None, mobile_emulation: dict = None, **kwargs):
        chrome_options = cls._get_chrome_options(headless, options, mobile_emulation)
        service = ChromeService(cls._get_driver_path("chrome", execute_path))
        chrome_driver = Chrome(service=service, options=chrome_options, **kwargs)
        logger.info(f'{Emoji.CHECK_MARK_BUTTON} started chrome successfully.')
        return chrome_driver

    @classmethod
    def firefox(cls, headless=False, execute_path=None, options: FirefoxOptions = None, **kwargs):
        firefox_options = cls._get_firefox_options(headless, options)
        service = FirefoxService(cls._get_driver_path("firefox", execute_path))
        firefox_driver = Firefox(service=service, options=firefox_options, **kwargs)
        logger.info(f'{Emoji.CHECK_MARK_BUTTON} started firefox successfully.')
        return firefox_driver

    @staticmethod
    def _get_firefox_options(headless, options):
        options = FirefoxOptions() if options is None else options
        if headless:
            options.add_argument('--headless')
        return options

    @staticmethod
    def _get_chrome_options(headless, options, mobile_emulation):
        options = ChromeOptions() if options is None else options
        options.add_argument('--disable-gpu')  # 禁用 GPU 加速
        options.add_argument('--disable-extensions')  # 禁用扩展
        options.add_argument('--disable-dev-shm-usage')  # 禁用 /dev/shm 临时文件系统
        if headless:
            options.add_argument('--headless')
        elif mobile_emulation:
            # mobile_emulation = {"deviceName": "iPhone 8"}
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        return options


if __name__ == '__main__':
    # mobile_emulation = {"deviceName": "iPhone 8"}
    driver = Browsers.chrome()
    driver.get("https://httpbin.org/#/")
    driver.quit()

