# -*- coding: UTF-8 -*-
# @Project: helium
# @File: assertions
# @Author：Lucas Liu
# @Time: 2022/10/11 10:27 AM
# @Software: PyCharm
from selenium.webdriver.remote.webdriver import WebDriver
import re
from typing import TypedDict


class ExpectOptions(TypedDict, total=False):
    is_contain: bool
    expected_text: str
    expected_number: int


class BaseAssertions(object):

    def __init__(self, is_not: bool = False) -> None:
        self._is_not = is_not

    def _expect_impl(self, actual, message, expect_options: ExpectOptions = None):
        expected = expect_options.get('expected_text') if expect_options else None
        is_contain = expect_options.get('is_contain') if expect_options else None
        expected_number = expect_options.get('expected_number') if expect_options else None
        if expected and isinstance(expected, re.Pattern):
            match = re.findall(expected, actual)
            expected = f"{match[0] if match else ''}"
            result = True if match else False
        elif expect_options is None:
            result = actual
        elif expected_number:
            result = actual == expected_number
        else:
            result = expected in actual if is_contain else actual == expected
        if self._is_not:
            message = message.replace("expected to", "expected not to")
            result = not result
        expected = expected or expected_number
        assert result, f"{message} {expected if expected else ''}, the actual is: {actual}"


class PageAssertions(BaseAssertions):
    def __init__(self, driver: WebDriver, is_not: bool = False):
        super(PageAssertions, self).__init__(is_not)
        self._driver = driver

    @property
    def _not(self) -> "PageAssertions":
        return PageAssertions(self._driver, not self._is_not)

    def to_have_title(self, expected):
        title = self._driver.title
        self._expect_impl(title, "Page title expected to be:", ExpectOptions(expected_text=expected))

    def to_have_url(self, expected):
        url = self._driver.current_url
        self._expect_impl(url,  "Page url expected to be", ExpectOptions(expected_text=expected))

    def not_to_have_title(self, expected):
        self._not.to_have_title(expected)

    def not_to_have_url(self, expected):
        self._not.to_have_url(expected)


class ElemsAssertions(BaseAssertions):
    def __init__(self, elems, is_not: bool = False):
        super(ElemsAssertions, self).__init__(is_not)
        self._elems = elems

    @property
    def _not(self) -> "ElemsAssertions":
        return ElemsAssertions(self._elems, not self._is_not)

    def to_have_count(self, count):
        count_ = self._elems.count
        return self._expect_impl(count_, f'Elems expected to have count: ', ExpectOptions(expected_number=count))

    def not_to_have_count(self, count):
        self._not.to_have_count(count)


class ElemAssertions(BaseAssertions):

    def __init__(self, elem, is_not: bool = False):
        super(ElemAssertions, self).__init__(is_not)
        self._elem = elem

    @property
    def _not(self) -> "ElemAssertions":
        return ElemAssertions(self._elem, not self._is_not)

    def to_be_checked(self):
        checked = self._elem.is_selected()
        self._expect_impl(checked, "Elem expected to be checked")

    def not_to_be_checked(self):
        self._not.to_be_checked()

    def to_be_disabled(self):
        disable = not self._elem.elem.is_enabled()
        self._expect_impl(disable, "Elem expected to be disable")

    def not_to_be_disable(self):
        self._not.to_be_disabled()

    def to_be_editable(self):
        editable = self._elem.elem.is_enabled()
        self._expect_impl(editable, "Elem expected to be editable")

    def not_to_be_editable(self):
        self._not.to_be_editable()

    def to_be_empty(self):
        empty = self._elem.elem.get_property('textContent')
        self._expect_impl(bool(empty), "Elem expected to be empty")

    def not_to_be_empty(self):
        self._not.to_be_empty()

    def to_be_enable(self):
        enable = self._elem.elem.is_enabled()
        self._expect_impl(enable, "Elem expected to be enable")

    def not_to_be_enable(self):
        self._not.to_be_enable()

    def to_be_exist(self):
        exist = self._elem.is_exist()
        self._expect_impl(exist, "Elem expected to be exist")

    def not_to_be_exist(self):
        self._not.to_be_exist()

    def to_be_visible(self):
        visible = self._elem.is_visible()
        self._expect_impl(visible, "Elem expected to be visible")

    def not_to_be_visible(self):
        self._not.to_be_visible()

    def to_contain_text(self, expected):
        text = self._elem.text
        self._expect_impl(text,  "Elem expected to contain text:", ExpectOptions(expected_text=expected, is_contain=True))

    def not_to_contain_text(self, expected):
        self._not.to_contain_text(expected)

    def to_have_attribute(self, name, value):
        attribute = self._elem.get_attribute(name)
        self._expect_impl(attribute,  "Elem expected to attribute:", ExpectOptions(expected_text=value))

    def not_to_have_attribute(self, name, value):
        self._not.to_have_attribute(name, value)

    def to_have_class(self, expected):
        class_ = self._elem.get_attribute('class')
        self._expect_impl(class_,  "Elem expected to class_:", ExpectOptions(expected_text=expected))

    def not_to_have_class(self, expected):
        self._not.to_have_class(expected)

    def to_have_text(self, expected):
        text = self._elem.text
        self._expect_impl(text, "Elem expected to have text:", ExpectOptions(expected_text=expected, is_contain=False))

    def not_to_have_text(self, expected):
        self._not.to_have_text(expected)
