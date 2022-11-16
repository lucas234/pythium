# @Project: pythium
# @Author：Lucas Liu
# @Time: 2022/10/28 9:15 AM
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from functools import wraps
from selenium.webdriver.remote.webdriver import WebDriver
from appium.webdriver.webdriver import WebDriver as MobileDriver
from typing import Union, List, Callable, Any
import inspect
from abc import abstractmethod
from selenium.webdriver.remote.webelement import WebElement
from appium.webdriver.webelement import WebElement as MobileElement


_LOCATORS = {
            # selenium locators
            'css': By.CSS_SELECTOR,
            'id_': By.ID,
            'name': By.NAME,
            'xpath': By.XPATH,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT,
            'tag_name': By.TAG_NAME,
            'class_name': By.CLASS_NAME,
            # appium locators
            "ios_predicate": AppiumBy.IOS_PREDICATE,
            "ios_uiautomation": AppiumBy.IOS_UIAUTOMATION,
            "ios_class_chain": AppiumBy.IOS_CLASS_CHAIN,
            "android_uiautomator": AppiumBy.ANDROID_UIAUTOMATOR,
            "android_viewtag": AppiumBy.ANDROID_VIEWTAG,
            "android_data_matcher": AppiumBy.ANDROID_DATA_MATCHER,
            "android_view_matcher": AppiumBy.ANDROID_VIEW_MATCHER,
            # Deprecated
            "windows_ui_automation": AppiumBy.WINDOWS_UI_AUTOMATION,
            "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
            "image": AppiumBy.IMAGE,
            "custom": AppiumBy.CUSTOM,
            }


def _get_kwargs():
    frame = inspect.currentframe().f_back
    keys, _, _, values = inspect.getargvalues(frame)
    kwargs = {}
    for key in keys:
        if key != 'self':
            kwargs[key] = values[key]
    return kwargs


def _valid_locator(_kwargs):
    if len(_kwargs) != 1:
        raise Exception("Only support one locate strategy, please have a check!")
    (k, v), = _kwargs.items()
    if k not in _LOCATORS.keys():
        raise Exception(f"NotSupport({k}='{v}'), Only support the following locators: {list(_LOCATORS.keys())}")
    locator = (_LOCATORS[k], v)
    return locator


def _get_func_kwargs(args_, kwargs_, func):
    default_kwargs = inspect.signature(func).parameters
    keys = list(default_kwargs.keys())[1:]
    if len(args_) == len(keys):
        return dict(zip(list(keys), args_))
    if len(kwargs_) == len(keys):
        return kwargs_
    default_keys = keys[len(args_):]
    default_keys = [i for i in default_keys if i not in kwargs_]
    new_kwargs_ = dict(zip(list(keys), args_))
    for key in default_keys:
        new_kwargs_[key] = default_kwargs.get(key).default
    kwargs_.update(new_kwargs_)
    return kwargs_


def _handle_return_type(return_type, driver: WebDriver, locator):
    if return_type in [List[WebElement], List[MobileElement]]:
        return driver.find_elements(*locator)
    elif return_type in [WebElement, MobileElement]:
        return driver.find_element(*locator)
    else:
        raise Exception("Only support the WebElement and [WebElement]!")


def find_by(id_=None, css=None, name=None, xpath=None, partial_link_text=None,
            link_text=None, class_name=None, tag_name=None) -> Callable[[], Any]:
    """ find webElement by locator(selenium)"""
    _locators = {k: v for k, v in _get_kwargs().items() if v}
    _by, value = _valid_locator(_locators)

    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            func_kwargs = _get_func_kwargs(args[1:], kwargs, func)
            locator = (_by, value.format(**func_kwargs))
            browser_name = args[0].driver.capabilities.get('browserName')
            device_name = args[0].driver.capabilities.get('deviceName')
            browsers = ['chrome', 'firefox', 'safari', 'ie', 'edge', 'opera']
            if not device_name and browser_name.lower() in browsers:
                args[0].locators[func.__name__] = locator
                return_type = inspect.signature(func).return_annotation
                return _handle_return_type(return_type, args[0].driver, locator)
            else:
                return func(*args, **kwargs)
        return wrapped_func
    return decorator


def _find_by(platform):
    def __find_by(id_=None, css=None, name=None, xpath=None, partial_link_text=None,
                  link_text=None, class_name=None, tag_name=None, ios_predicate=None,
                  android_uiautomator=None, android_viewtag=None, android_data_matcher=None,
                  android_view_matcher=None, windows_ui_automation=None, accessibility_id=None,
                  ios_uiautomation=None, ios_class_chain=None, image=None, custom=None) -> Callable[[], Any]:
        """ find mobileElement by locator(appium)"""
        _locators = {k: v for k, v in _get_kwargs().items() if v}
        locator = _valid_locator(_locators)

        def decorator(func):
            @wraps(func)
            def wrapped_func(*args, **kwargs):
                platform_name = args[0].driver.capabilities.get('platformName')
                if platform_name.lower() == platform.lower():
                    args[0].locators[func.__name__] = locator
                    return args[0].driver.find_element(*locator)
                else:
                    return func(*args, **kwargs)
            return wrapped_func
        return decorator
    return __find_by


ios_find_by = _find_by(platform="ios")
android_find_by = _find_by(platform="android")


def by(id_=None, css=None, name=None, xpath=None, partial_link_text=None,
       link_text=None, class_name=None, tag_name=None, image=None, custom=None,
       android_uiautomator=None, android_viewtag=None, android_data_matcher=None,
       android_view_matcher=None, windows_ui_automation=None, accessibility_id=None,
       ios_uiautomation=None, ios_class_chain=None, ios_predicate=None):
    _locators = {k: v for k, v in _get_kwargs().items() if v}
    _valid_locator(_locators)
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

    def goto(self, url):
        self.driver.get(url)
        return self

    @abstractmethod
    def _is_loaded(self):
        pass

