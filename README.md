#### Pythium 
***
Python based Page Factory design pattern test library, similar to Java's Page Factory pattern, 
designed to reduce code redundancy, easy to use, are very descriptive， make the code more 
readable and understandable and with a high degree of scalability.

- Supports locate element with annotation
- Supports multiple positioning methods for the same element
- Supports dynamically locate element

#### Install
***
`pip install pythium`

#### Usage
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
    @android_find_all(by(android_uiautomator='resourceId("com.app:id/search_txtbox")'),
                      by(android_uiautomator='resourceId("com.app:id/search_txtbox")'))
    def find_all_mobile_test(self) -> WebElement: return Any

    # for dynamical locator
    @find_by(xpath="//div[{n}]/a[{k}]/div[{m}]/{f}")
    @ios_find_by(xpath="//div[1]/a[{n}]/div[{k}]")
    def dynamical_locator(self, n, k, m=4, f=6) -> WebElement: ...

    # for list WebElements
    @find_by(css=".login")
    def list_web_elements(self) -> List[MobileElement]: ...

    def _is_loaded(self):
        print("implement something...")


if __name__ == '__main__':
    from selenium import webdriver

    driver = webdriver.Chrome()
    login = LoginPage(driver)
    # no @property
    login.search_input().click()
    # with @property
    login.search_input_with_property.click()
    # for dynamical locator
    login.dynamical_locator(2, 3, 4, 5).click()
    # for list WebElement
    print(len(login.list_web_elements()))
```

The`@find_all`, `@ios_find_all`, `@android_find_all` annotations locates the web element using more than one criteria, 

given that at least one criteria match. it uses an OR conditional relationship between the multiple `@xxx_find_by`.

example: `@find_all(by(css=".icon-logo1"), by(id="icon"))` 

first will find element `by(css=".icon-logo1")`, if found, return `WebElement`; 

if not found, will find element `by(id="icon")`, if found, return `WebElement`, if not found, will raise `Exception`.
 
