# @Project: pythium
# @File: utils
# @Author：Lucas Liu
# @Time: 2022/12/9 9:25 AM
# @Software: PyCharm
import re
import inspect
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By


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


class Utils:

    @staticmethod
    def remove_scheme(url):
        return re.sub(r"https?://", "", url)

    @staticmethod
    def get_kwargs():
        frame = inspect.currentframe().f_back
        keys, _, _, values = inspect.getargvalues(frame)
        kwargs = {}
        for key in keys:
            if key != 'self':
                kwargs[key] = values[key]
        return kwargs

    @staticmethod
    def valid_locator(_kwargs):
        if len(_kwargs) != 1:
            raise Exception("Only support one locate strategy, please have a check!")
        (k, v), = _kwargs.items()
        if k not in _LOCATORS.keys():
            raise Exception(f"NotSupport({k}='{v}'), Only support the following locators: {list(_LOCATORS.keys())}")
        # locator = (_LOCATORS[k], v)
        # return locator
        return _LOCATORS[k], v, k

    @staticmethod
    def get_func_kwargs(args_, kwargs_, func):
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


if __name__ == '__main__':
    pass
