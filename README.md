<!-- README.zh.md -->
#### Pythium 
[中文](README.md) | [English](README.en.md)

基于 Python 的 Page Factory 设计模式测试库, 类似于Java的Page Factory模式，旨在减少代码冗余，简单易用，具有高度的可扩展能力。

- 支持以@annotation的方式定义元素
- 支持同一个元素多种定位方式
- 支持动态的定位方式

#### 安装

`pip install pythium`

#### 用法

1. 使用单个定位元素
   - `find_by`
   - `ios_find_by`
   - `android_find_by`
   
   `find_by`用于`Web`平台, 

   `ios_find_by`和`android_find_by`分别适用于苹果和安卓平台;

   例子: `find_by(css=".search")`

2. 使用多个定位元素，元素之间为`or`的关系，按顺序查找:
   - `find_all`
   - `ios_find_all`
   - `android_find_all`
   
   例子: `@find_all(by(css=".icon-logo1"), by(id="icon"))` ;

   首先查找元素 `by(css=".icon-logo1")`, 如果找到则返回 `WebElement`;

   如果没找到则通过 `by(id="icon")`继续找, 如果找到则返回`WebElement`;

   最后没找到则抛出异常 `Exception`.

3. `Page object`代码样例:
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
        def list_web_elements(self) -> List[MobileElement]: ...
    
        def _is_loaded(self):
            print("implement something...")
    
    if __name__ == '__main__':
        from pythium import Browser
        driver = Browser.chrome()
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
4. 非`Page object`代码样例:
    ```python
    from pythium import Falcon, Element, Page
    from pythium import Browser

    driver = Browser.chrome()
    Ele = Falcon(Element, driver)
    page = Page(driver)
    page.goto("https://www.baidu.com/")
    search_input = Ele(id_="kw")
    search_button = Ele(id_='su')
    search_input.send_keys("selenium")
    search_button.click()
    page.wait(5).expect.to_have_title("selenium_百度搜索")
    ```

#### 使用自定义`Element`
   使用自定义`Element`的好处是，不用额外的封装一些公用的方法(额外的等待、元素是否存在等)；

   **如果遇到一些无法处理的或者没有的方法，则需要根据自己的需求，继承`Element`类，定义自己的方法调用即可**

   使用时只需把函数返回类型定义为`Element, Elements`(`或者自定义的类名`),替换`WebElement, MobileElement`
   
   代码样例：

   ```python
   from pythium import find_by, find_all
from pythium import Page, by, Element, Elements
from typing import Any
from pythium import Browser


class BaiDuPage(Page):

    def _is_loaded(self):
        pass

    @property
    @find_by(id_="kw")
    def search_input(self) -> Element: ...

    @property
    @find_by(id_='su')
    def search_button(self) -> Element: ...

    @find_by(id_="kw")
    def search_input_no_property(self) -> Element: return Any

    @property
    @find_all(by(id_="kw"), by(css=".s_ipt"))
    def search_input_find_all(self) -> Element: ...

    # for dynamical locator
    @property
    @find_by(xpath="//div[{n}]/a[{k}]/div[{m}]/{f}")
    # @find_by(xpath="//div[1]/a[2]/div[3]/")
    def dynamical_locator(self, n, k, m=4, f=6) -> Element: ...

    # for list Elements
    @property
    @find_by(css=".mnav")
    def list_elements(self) -> Elements: ...


if __name__ == '__main__':
    driver = Browser().chrome()
    baidu = BaiDuPage(driver)
    baidu.goto("https://www.baidu.com/")
    print(baidu.list_elements.index(0).text)
    baidu.search_input.send_keys("selenium")
    # baidu.search_input_no_property().send_keys("selenium")
    baidu.search_button.click()
    baidu.wait(5).expect.to_have_title('selenium_百度搜索')
   ```

#### 元素定位参考

- [Css 用法](./docs/locator%20cheat%20sheet/Css%20cheat%20sheet.md)
- [Xpath 用法](./docs/locator%20cheat%20sheet/Xpath%20cheat%20sheet.md)