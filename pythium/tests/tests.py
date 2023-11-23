# -*- coding: UTF-8 -*-
# @Project: pyium
# @File: test
# @Author：Lucas Liu
# @Time: 2023/9/15 13:37
# @Software: PyCharm
from pythium import Falcon, Element, Page
from pythium import Browsers


def web_test():
    driver = Browsers.chrome()
    Elem = Falcon(Element, driver)
    page = Page(driver)
    page.goto("https://www.baidu.com/")
    Elem(id_="kw").send_keys("selenium")
    Elem(id_='su').click()
    page.wait(5).expect.to_have_title("selenium_百度搜索")
    driver.quit()


if __name__ == '__main__':
    web_test()
