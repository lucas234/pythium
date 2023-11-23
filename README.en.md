<!-- README.md -->
#### Pythium 
[中文](README.md) | [English](README.en.md)

Python based Page Factory design pattern test library, similar to Java's Page Factory pattern, 
designed to reduce code redundancy, easy to use, are very descriptive， make the code more 
readable and understandable and with a high degree of scalability.

- Supports locate element with annotation
- Supports multiple positioning methods for the same element
- Supports dynamically locate element

#### Install

`pip install pythium`

#### Usage

1. Using a single locator element
   - `find_by`
   - `ios_find_by`
   - `android_find_by`
   
   `find_by` is used for `Web` platform, 

   `ios_find_by` and `android_find_by` are applicable to the iOS and Android platforms respectively.

   sample: `find_by(css=".search")`

2. Use multiple locator elements with an 'or' relationship between elements, searching in order:
   - `find_all`
   - `ios_find_all`
   - `android_find_all`
   
   sample: `@find_all(by(css=".icon-logo1"), by(id="icon"))` ;

   First, locate the element by `by(css=".icon-logo1")`; If found, return the `WebElement`.

   If not found, then continue by locating the element using `by(id="icon")`. If found, return the `WebElement`.

   If still not found, throw an `Exception`.

3. `Page object` code sample:
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
        from pythium import Browsers
        driver = Browsers.chrome()
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
4. Not `Page object` code sample:
    ```python
    from pythium import Falcon, Element, Page
    from pythium import Browsers

    driver = Browsers.chrome()
    Ele = Falcon(Element, driver)
    page = Page(driver)
    page.goto("https://www.baidu.com/")
    search_input = Ele(id_="kw")
    search_button = Ele(id_='su')
    search_input.send_keys("selenium")
    search_button.click()
    page.wait(5).expect.to_have_title("selenium_百度搜索")
    ```

#### Using a custom `Element`

   The advantage of using a custom Element is that there is no need to encapsulate additional common methods (extra waits, checking element existence, etc.).

   If there are some methods that cannot be handled or are not available, you can inherit from the Element class according to your needs and define your own methods.

   When using it, simply define the return type of the function as Element or Elements (or your custom class name), replacing WebElement or MobileElement.

   sample：

   ```python
   from pythium import find_by, find_all
   from pythium import Page, by, Element, Elements
   from typing import Any
   from pythium import Browsers


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
       driver = Browsers().chrome()
       baidu = BaiDuPage(driver)
       baidu.goto("https://www.baidu.com/")
       print(baidu.list_elements.index(0).text)
       baidu.search_input.send_keys("selenium")
       # baidu.search_input_no_property().send_keys("selenium")
       baidu.search_button.click()
       baidu.wait(5).expect.to_have_title('selenium_百度搜索')
   ```

#### Element locators reference

- [Css usage](./docs/locator%20cheat%20sheet/Css%20cheat%20sheet.md)
- [Xpath usage](./docs/locator%20cheat%20sheet/Xpath%20cheat%20sheet.md)