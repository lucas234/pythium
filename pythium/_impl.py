# @Project: pythium
# @Author：Lucas Liu
# @Time: 2022/10/28 9:15 AM
from selenium.common.exceptions import NoSuchElementException
from functools import wraps
from appium.webdriver.webdriver import WebDriver as MobileDriver
from typing import Union, Callable, Any
import inspect
from abc import abstractmethod
from selenium.webdriver.remote.webdriver import WebDriver
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from appium.webdriver.webelement import WebElement as MobileElement
from pythium.objects import Element, Elements
from pythium.actions import Actions
from pythium.utils import Utils
from pythium.assertions import PageAssertions
from pythium.http_session import HttpSession
from pythium.emoji import Emoji
from loguru import logger


def _handle_return_type(return_type, driver: WebDriver, locator):
    if return_type in [List[WebElement], List[MobileElement]]:
        return driver.find_elements(*locator[0])
    elif return_type in [WebElement, MobileElement]:
        return driver.find_element(*locator[0])
    elif issubclass(return_type, Element) or issubclass(return_type, Elements):
        return return_type(**locator[1], driver=driver)
    else:
        raise Exception(f"{Emoji.EXCEPTION} Only support the WebElement, [WebElement], Element and Elements!")


def find_by(id_=None, css=None, name=None, xpath=None, partial_link_text=None,
            link_text=None, class_name=None, tag_name=None) -> Callable[[], Any]:
    """ find webElement by locator(selenium)"""
    _locators = {k: v for k, v in Utils.get_kwargs().items() if v}
    _by, value, key = Utils.valid_locator(_locators)

    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            func_kwargs = Utils.get_func_kwargs(args[1:], kwargs, func)
            locator = (_by, value.format(**func_kwargs)), {key: value}
            if args[0].action.is_web_platform:
                args[0].locators[func.__name__] = locator[0]
                return_type = inspect.signature(func).return_annotation
                return _handle_return_type(return_type, args[0].driver, locator)
            else:
                return func(*args, **kwargs)
        return wrapped_func
    return decorator


def _appium_find_by(platform):
    def _find_by(id_=None, css=None, name=None, xpath=None, partial_link_text=None,
                 link_text=None, class_name=None, tag_name=None, ios_predicate=None,
                 android_uiautomator=None, android_viewtag=None, android_data_matcher=None,
                 android_view_matcher=None, windows_ui_automation=None, accessibility_id=None,
                 ios_uiautomation=None, ios_class_chain=None, image=None, custom=None) -> Callable[[], Any]:
        """ find mobileElement by locator(appium)"""
        _locators = {k: v for k, v in Utils.get_kwargs().items() if v}
        _by, value, key = Utils.valid_locator(_locators)

        def decorator(func):
            @wraps(func)
            def wrapped_func(*args, **kwargs):
                func_kwargs = Utils.get_func_kwargs(args[1:], kwargs, func)
                locator = (_by, value.format(**func_kwargs)), {key: value}
                if args[0].action.is_platform(platform):
                    args[0].locators[func.__name__] = locator[0]
                    return_type = inspect.signature(func).return_annotation
                    return _handle_return_type(return_type, args[0].driver, locator)
                else:
                    return func(*args, **kwargs)
            return wrapped_func
        return decorator
    return _find_by


ios_find_by = _appium_find_by('ios')
android_find_by = _appium_find_by('android')


def by(id_=None, css=None, name=None, xpath=None, partial_link_text=None,
       link_text=None, class_name=None, tag_name=None, image=None, custom=None,
       android_uiautomator=None, android_viewtag=None, android_data_matcher=None,
       android_view_matcher=None, windows_ui_automation=None, accessibility_id=None,
       ios_uiautomation=None, ios_class_chain=None, ios_predicate=None):
    _locators = {k: v for k, v in Utils.get_kwargs().items() if v}
    Utils.valid_locator(_locators)
    return _locators


def _find_all(by_: Union[find_by, ios_find_by, android_find_by]):
    def __find_all(*strategies: by):
        """ find webElement by chain"""
        def decorator(func):
            @wraps(func)
            def wrapped_func(*args, **kwargs):
                exceptions = []
                for strategy in strategies:
                    try:
                        elem = by_(**strategy)(func)(*args, **kwargs)
                        return elem
                    except NoSuchElementException as e:
                        exceptions.append(e)
                        print(e.msg)
                else:
                    if exceptions:
                        raise exceptions[-1]
            return wrapped_func
        return decorator
    return __find_all


find_all = _find_all(find_by)
ios_find_all = _find_all(ios_find_by)
android_find_all = _find_all(android_find_by)


class Page:
    def __init__(self, driver_: Union[MobileDriver, WebDriver]):
        self.driver = driver_
        self.locators = {}
        self.action = Actions(self.driver)

    @abstractmethod
    def _is_loaded(self):
        pass

    def goto(self, url):
        self.driver.get(url)
        logger.info(f"{Emoji.LINK} navigate to {url}.")
        return self

    def wait(self, seconds=5):
        self.action.wait(seconds)
        return self

    def open_deeplink(self, link, ios_bundle_id=None):
        self.action.open_deep_link(link, ios_bundle_id)
        logger.info(f"{Emoji.LINK} open deeplink: {link}.")
        return self

    @property
    def expect(self) -> PageAssertions:
        return PageAssertions(self.driver)

    @property
    def request(self):
        session = HttpSession()
        session.cookies.update(self._get_cookies())
        return session

    def _get_cookies(self) -> dict:
        cookies = {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}
        return cookies


# not for PO
def falcon(f, driver=None):
    def _find_by(id_=None, css=None, name=None, xpath=None, partial_link_text=None, link_text=None,
                 class_name=None, tag_name=None, image=None, custom=None, android_uiautomator=None,
                 android_viewtag=None, android_data_matcher=None, android_view_matcher=None,
                 windows_ui_automation=None, accessibility_id=None, ios_uiautomation=None,
                 ios_class_chain=None, ios_predicate=None) -> Union[Element, Elements]:
        kwargs = Utils.get_kwargs()
        kwargs = {k: v for k, v in kwargs.items() if v}
        Utils.valid_locator(kwargs)

        def decorator(func):
            kwargs['driver'] = driver
            return func(**kwargs)
        return decorator(f)
    return _find_by


Falcon = falcon
