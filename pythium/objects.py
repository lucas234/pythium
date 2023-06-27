# -*- coding: UTF-8 -*-
# @Project: gls.automation.python
# @File: elem
# @Author：Lucas Liu
# @Time: 2022/11/25 10:55 AM
# @Software: PyCharm
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from retrying import retry
from typing import Literal
from pythium.utils import Utils
from pythium.actions import Actions
from pythium.assertions import ElemAssertions, ElemsAssertions


def retry_if_exceptions(exception):
    exceptions = [ElementClickInterceptedException, StaleElementReferenceException,
                  ElementNotVisibleException, NoSuchElementException]
    return any([isinstance(exception, e) for e in exceptions])


class Elements:

    _TIMEOUT = 8

    def __init__(self, id_=None, css=None, name=None, xpath=None, partial_link_text=None, link_text=None,
                 class_name=None, tag_name=None, image=None, custom=None, android_uiautomator=None,
                 android_viewtag=None, android_data_matcher=None, android_view_matcher=None,
                 windows_ui_automation=None, accessibility_id=None, ios_uiautomation=None, ios_class_chain=None,
                 ios_predicate=None, driver: WebDriver = None):
        _locators = {k: v for k, v in Utils.get_kwargs().items() if v}
        if 'driver' in _locators:
            _locators.pop('driver')
        self._locator = Utils.valid_locator(_locators)[:2]
        self._driver = driver
        if driver:
            self._action = Actions(self._driver)
            self.elems = self._find_elements()

    def __get__(self, obj, owner):
        """Gets the element object"""
        self._driver = obj.driver
        self._action = Actions(self._driver)
        self.elems = self._find_elements()
        return self

    def _find_elements(self, timeout=_TIMEOUT):
        try:
            return WebDriverWait(self._driver, timeout).until(ec.presence_of_all_elements_located(self._locator))
        except TimeoutException as te:
            print(te)
            return self._driver.find_elements(*self._locator)
        except NoSuchElementException as nse:
            print(nse)
            return self._driver.find_elements(*self._locator)

    @property
    def expect(self) -> ElemsAssertions:
        return ElemsAssertions(self)

    @property
    def count(self):
        return len(self.elems)

    def index(self, n):
        return self.elems[n]

    def wait(self, seconds=5):
        self._action.wait(seconds)
        return self

    @property
    def texts(self):
        if self._action.is_web_platform:
            return [elem.get_attribute('textContent') for elem in self.elems]
        if self._action.is_mobile_platform:
            return [elem.text for elem in self.elems]


class Element:

    _TIMEOUT = 8

    def __init__(self, id_=None, css=None, name=None, xpath=None, partial_link_text=None, link_text=None,
                 class_name=None, tag_name=None, image=None, custom=None, android_uiautomator=None,
                 android_viewtag=None, android_data_matcher=None, android_view_matcher=None,
                 windows_ui_automation=None, accessibility_id=None, ios_uiautomation=None, ios_class_chain=None,
                 ios_predicate=None, driver: WebDriver = None):
        _locators = {k: v for k, v in Utils.get_kwargs().items() if v}
        if 'driver' in _locators:
            _locators.pop('driver')
        self._locator = Utils.valid_locator(_locators)[:2]
        self._driver = driver
        if driver:
            self._action = Actions(self._driver)
            self.elem = self._find_element()

    def __get__(self, obj, owner):
        """Gets the element object"""
        self._driver = obj.driver
        self._action = Actions(self._driver)
        self.elem = self._find_element()
        return self

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        self.__get__(obj, obj.__class__)
        self._find_element().clear()
        self._find_element().send_keys(value)

    @property
    def expect(self) -> ElemAssertions:
        return ElemAssertions(self)

    def _find_element(self, timeout=_TIMEOUT):
        try:
            elem = WebDriverWait(self._driver, timeout).until(ec.presence_of_element_located(self._locator))
            self._action.highlight(elem)
            return elem
        except TimeoutException as te:
            print(te)
            elem = self._driver.find_element(*self._locator)
            self._action.highlight(elem)
            return elem
        except NoSuchElementException as nse:
            print(nse)
            elem = self._driver.find_element(*self._locator)
            self._action.highlight(elem)
            return elem

    def wait_until_visible(self, timeout=_TIMEOUT, throw_exception=True):
        self._action.wait_util(self._locator, ec.visibility_of_element_located, timeout, throw_exception)
        return self

    def wait_util_clickable(self, timeout=_TIMEOUT, throw_exception=True):
        self._action.wait_util(self._locator, ec.element_to_be_clickable, timeout, throw_exception)
        return self

    def wait(self, seconds=5):
        self._action.wait(seconds)
        return self

    def is_visible(self, timeout=_TIMEOUT):
        return self._action.is_(self._locator, ec.visibility_of_element_located, timeout)

    def is_selected(self, timeout=_TIMEOUT):
        return self._action.is_(self._locator, ec.element_located_to_be_selected, timeout)

    def is_disappeared(self, timeout=_TIMEOUT):
        return self._action.is_(self._locator, ec.invisibility_of_element_located, timeout)

    def is_exist(self, timeout=_TIMEOUT):
        try:
            self._find_element(timeout)
            return True
        except Exception as ex:
            by, value = self._locator
            print(f"element: by.{by}={value} is not exist! original exception: {ex}")
            return False

    def clear(self):
        self._find_element().clear()
        return self

    def click_if_exist(self, timeout=_TIMEOUT, by: Literal['js', 'default', 'action'] = 'default'):
        if self.is_exist(timeout):
            self.click(by)
        return self

    @retry(retry_on_exception=retry_if_exceptions, stop_max_attempt_number=2, wait_fixed=1000)
    def click(self, by: Literal['js', 'default', 'action'] = 'default'):
        if by == "js":
            # only support web
            if self._action.is_web_platform:
                self._driver.execute_script("arguments[0].click();", self.elem)
            else:
                raise Exception("Clicking element by js only support web platform")
        elif by == 'action':
            self.w3c_actions.pointer_action.click(self.elem)
            self.w3c_actions.perform()
        elif by == 'default':
            self._find_element().click()
        else:
            raise Exception("'by' only support the following strategies: ['js', 'default', 'action']")
        return self

    def send_keys(self, value):
        self._find_element().send_keys(value)
        return self

    def get_attribute(self, name):
        return self._find_element().get_attribute(name)

    def get_property(self, name):
        return self._find_element().get_property(name)

    @property
    def text(self):
        if self._action.is_web_platform:
            return self._find_element().get_attribute('textContent')
        if self._action.is_mobile_platform:
            return self._find_element().text

    def scroll_into_view(self, direction='down', swipe_max_times=5, top_offset=100, bottom_offset=100):
        if self._action.is_web_platform:
            self._driver.execute_script("arguments[0].scrollIntoView(true);", self.elem)
        if self._action.is_mobile_platform:
            self._action.scroll_into_view(self._locator, direction, swipe_max_times, top_offset, bottom_offset)
        return self

    def switch_to_iframe(self, timeout=_TIMEOUT):
        WebDriverWait(self._driver, timeout).until(ec.frame_to_be_available_and_switch_to_it(self._locator))

    def switch_to_default_content(self):
        self._driver.switch_to.default_content()
        return self

    @property
    def w3c_actions(self):
        actions = ActionChains(self._driver)
        actions.w3c_actions = ActionBuilder(self._driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        return actions.w3c_actions
