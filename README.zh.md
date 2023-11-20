<!-- README.zh.md -->
#### Pythium 
[English Version](README.md) | [中文版](README.zh.md)
***
基于 Python 的 Page Factory 设计模式测试库, 类似于Java的Page Factory模式，旨在减少代码冗余，简单易用，具有高度的可扩展能力。

- 支持以@annotation的方式定义元素
- 支持同一个元素多种定位方式
- 支持动态的定位方式

#### 安装
***
`pip install pythium`

#### 用法
***
```python
from pythium import find_by, android_find_by, ios_find_by
from pythium import find_all, ios_find_all, android_find_all, Page, by
from appium.webdriver.webelement import WebElement as MobileElement
from selenium.webdriver.remote.webelement import WebElement
from typing import Any, List


class LoginPage(Page):

    @find_by(css=".search")
    @ios_find_by(ios_predicate='value == "Search something"')
    @android_find_by(android_uiautomator='resourceId("com.app:id/search_txtbox")')
    def search_input(self) -> WebElement: ...

    @property
    @find_by(css=".search")
    @ios_find_by(ios_predicate='value == "Search something"')
    @android_find_by(android_uiautomator='resourceId("com.app:id/search_txtbox")')
    def search_input_with_property(self) -> WebElement: ...

    @property
    @find_all(by(css=".icon-logo1"), by(css=".icon-logo"))
    def find_all_web_test(self) -> WebElement: return Any

    @property
    @ios_find_all(by(ios_predicate='value == "Search something"'), by(ios_predicate='value == "Search result"'))
    @android_find_all(by(android_uiautomator='resourceId("com.app:id/search_txtbox")'), by(android_uiautomator='resourceId("com.app:id/search_txtbox")'))
    def find_all_mobile_test(self) -> WebElement: return Any

    # for dynamical locator
    @find_by(xpath="//div[{n}]/a[{k}]/div[{m}]/{f}")
    @ios_find_by(xpath="//div[1]/a[{n}]/div[{k}]")
    def dynamical_locator(self, n, k, m=4, f=6) -> WebElement: ...

    # for list WebElements
    @find_by(css=".login")
    def list_web_elements(self) -> List[MobileElement]: ...```

    def _is_loaded(self):
        print("implement something...")

if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Chrome()
    login = LoginPage(driver)
    # no @property
    login.search_input.click()
    # with @property
    login.search_input_with_property.click()
    # for dynamical locator
    login.dynamical_locator(2, 3, 4, 5).click()
    # for list WebElement
    print(len(login.list_web_elements()))
```

`find_all`, `ios_find_all`, `android_find_all` 使用多个定位元素，元素之间为`or`的关系，按顺序查找

例子: `@find_all(by(css=".icon-logo1"), by(id="icon"))` 

首先查找元素 `by(css=".icon-logo1")`, 如果找到则返回 `WebElement`; 

如果没找到则通过 `by(id="icon")`继续找, 如果找到则返回`WebElement`, 最后没找到则抛出异常 `Exception`.
    