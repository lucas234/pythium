from pythium import Falcon, Element, Page
from pythium import Browser


class PageTests():

    @staticmethod
    def hover_and_click_test():
        driver = Browser.chrome()
        Elem = Falcon(Element, driver)
        page = Page(driver)
        page.goto('http://www.baidu.com')
        Elem(css='.mnav.s-top-more-btn').hover()
        Elem(xpath='//div[text()="百科"]').click()
        page.wait(5)
        page.quit()

    @staticmethod
    def web_test():
        driver = Browser.chrome()
        Elem = Falcon(Element, driver)
        page = Page(driver)
        page.goto('http://www.baidu.com')
        Elem(id_="kw").send_keys("selenium")
        Elem(id_='su').click('action')
        print(Elem(id_='su').get_property('value'))
        Elem(id_='su').expect.to_be_enable()
        page.wait(5).expect.to_have_title("selenium_百度搜索")
        page = Elem(id_='page')
        print(page.is_in_view())
        page.expect.not_to_be_in_view()
        page.scroll_into_view()
        print(page.is_in_view())
        page.expect.to_be_in_view()
        driver.quit()


if __name__ == '__main__':
    PageTests.web_test()
