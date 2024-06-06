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
    # baidu.search_input.send_keys("selenium")
    baidu.search_input.send_keys("selenium")
    # baidu.search_input_no_property().send_keys("selenium")
    baidu.search_button.click()
    baidu.wait(5).expect.to_have_title('selenium_百度搜索')
    driver.quit()