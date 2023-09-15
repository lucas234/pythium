# -*- coding: UTF-8 -*-
# @Project: CodeWarehouse
# @File: actions
# @Author：Lucas Liu
# @Time: 2022/1/19 4:00 下午
# @Software: PyCharm
from appium.webdriver import Remote
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from typing import NoReturn
import inspect
import time
from typing import Literal
from pythium.exceptions import IllegalArgumentException
from pythium.utils import Utils
from pythium.commands import IosCommands, AndroidCommands


class Actions(object):

    _TIMEOUT = 8

    def __init__(self, driver: Remote):
        self._driver = driver

    def wait_util(self, locator, ecs, timeout=_TIMEOUT, throw_exception=True):
        try:
            WebDriverWait(self._driver, timeout).until(ecs(locator))
        except TimeoutException as te:
            if throw_exception:
                raise te
            print(te)

    def is_(self, locator, ecs, timeout=_TIMEOUT):
        try:
            WebDriverWait(self._driver, timeout).until(ecs(locator))

            return True
        except TimeoutException as te:
            print(te)
            return False

    @property
    def is_mobile_platform(self):
        return self._driver.capabilities['platformName'].lower() in ['ios', 'android']

    @property
    def is_ios_platform(self):
        return self.is_platform('ios')

    @property
    def is_android_platform(self):
        return self.is_platform('android')

    def is_platform(self, platform: Literal['ios', 'android']):
        return self._driver.capabilities['platformName'].lower() == platform

    @property
    def is_web_platform(self):
        browser_name = self._driver.capabilities.get('browserName')
        device_name = self._driver.capabilities.get('deviceName')
        browsers = ['chrome', 'firefox', 'safari', 'ie', 'edge', 'opera']
        if not device_name and browser_name.lower() in browsers:
            return True
        else:
            return False

    def highlight(self, element, elapsed=800):
        """only support web UI"""
        if not self.is_web_platform:
            return
        previous_style = element.get_attribute("style")
        color = '#00cc66'
        style = f"arguments[0].setAttribute('style', 'border: 2px solid {color}; font-weight: bold;');"
        self._driver.execute_script(style, element)
        restore_script = f"var target = arguments[0];var previousStyle = arguments[1];" \
                         f"setTimeout(function(){{ target.setAttribute('style', previousStyle);}}, {elapsed});"
        # remove highlight
        self._driver.execute_script(restore_script, element, previous_style)

    def perform_search(self):
        if self.is_android_platform:
            self._driver.execute_script('mobile: performEditorAction', {'action': 'search'})
        elif self.is_ios_platform:
            self._driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Return").click()
            # input_element.send_keys("\n")
        else:
            msg = f"Only support the platforms: ['ios', 'android']!"
            raise IllegalArgumentException(msg)

    def swipe(self, direction: Literal["up", "down", "left", "right"], duration=800) -> NoReturn:
        sizes = tuple(self._driver.get_window_size().values())
        top_x = down_x = int(sizes[0] * 0.5)
        top_y = int(sizes[1] * 0.3)
        down_y = int(sizes[1] * 0.8)
        left_y = right_y = int(sizes[1] * 0.5)
        left_x = int(sizes[0] * 0.1)
        right_x = int(sizes[0] * 0.9)
        lines = {
            "up": (top_x, top_y, down_x, down_y),
            "down": (top_x, down_y, down_x, top_y),
            "left": (left_x, left_y, right_x, right_y),
            "right": (right_x, left_y, left_x, right_y)
        }
        if direction.lower() not in lines.keys():
            msg = f"{inspect.stack()[0][3]}('{direction}') only support the following params: {list(lines.keys())}!"
            raise IllegalArgumentException(msg)
        self._driver.swipe(*lines.get(direction.lower()), duration)

    def scroll_into_view(self, locator, direction='down', swipe_max_times=5, top_offset=100, bottom_offset=100):
        size = self._driver.get_window_size()
        print(f"screen size is: {size}")
        height = size['height']

        def location():
            try:
                _location = self._driver.find_element(*locator).location
                return _location['x'], _location['y']
            except Exception as e:
                _ = e
                return 0, 0

        def is_into_view():
            _x, _y = location()
            print(_x, _y)
            return top_offset < _y < height - bottom_offset and _x > 0

        def _swipe(direction_):
            for i in range(swipe_max_times):
                if is_into_view():
                    print(f"locator is into view: {locator}")
                    return
                x, y = location()
                self.swipe(direction_)
                new_x, new_y = location()
                if y == new_y and all([x, y, new_x, new_y]):
                    break

        reverse = {"down": "up", "up": "down"}
        _swipe(direction)
        if not is_into_view():
            _swipe(reverse[direction])

    def scroll_into_view_ios(self, locator):
        self._driver.find_element(*locator).click()
        self.wait(1)
        try:
            y = self._driver.find_element(*locator).rect['y']
            height = self._driver.get_window_size()["height"]
            if y > int(height*3/4):
                self.swipe('down')
            if int(height/4) > y:
                self.swipe('up')
        except NoSuchElementException:
            pass

    def open_deep_link(self, link: str, ios_bundle_id=None):
        """
        only for mobile platform
        """
        bundle_id = ios_bundle_id or self._driver.execute_script(f'mobile: {IosCommands.ActiveAppInfo}')['bundleId']

        def _by_safari(deep_link):
            prefix = f'{bundle_id}://'
            self._driver.execute_script(f'mobile: {IosCommands.TerminateApp}', {"bundleId": 'com.apple.mobilesafari'})
            self._driver.execute_script(f'mobile: {IosCommands.LaunchApp}', {"bundleId": 'com.apple.mobilesafari'})
            url_button = (AppiumBy.IOS_PREDICATE, 'type == "XCUIElementTypeButton" and name CONTAINS "URL" or label == "Address"')
            url_field = (AppiumBy.IOS_PREDICATE, 'type == "XCUIElementTypeTextField" and name CONTAINS "URL"')
            if not self._driver.is_keyboard_shown():
                time.sleep(4)
                self._driver.find_element(*url_button).click()
            self._driver.find_element(*url_field).send_keys(
                f'{prefix}{Utils.remove_scheme(deep_link)}\uE007')
            time.sleep(2)
            open_ = (AppiumBy.IOS_PREDICATE, 'name == "Open" AND type == "XCUIElementTypeButton"')
            self._driver.find_element(*open_).click()

        if self.is_ios_platform:
            self._driver.execute_script(f'mobile: {IosCommands.TerminateApp}', {"bundleId": bundle_id})
            # on ios platform, driver.get(link) only can use emulator
            # on real device, need to use other method
            is_simulator = self._driver.execute_script(f'mobile: {IosCommands.DeviceInfo}')['isSimulator']
            if is_simulator:
                self._driver.get(f'{bundle_id}://{Utils.remove_scheme(link)}')
            else:
                _by_safari(link)

        elif self.is_android_platform:
            self._driver.terminate_app(self._driver.current_package)
            # if driver.get(link) is not valid, then use execute_script
            self._driver.get(link)
            # driver.execute_script('mobile:deepLink', {'url': link, 'package': driver.current_package})
        else:
            raise Exception("Only support platforms: ['ios', 'android']")

    def scroll_into_view_android(self, locator):
        """
           only support AppiumBy.ANDROID_UIAUTOMATOR strategy
        """
        by, value = locator
        if 'uiautomator' not in by:
            raise IllegalArgumentException("only support AppiumBy.ANDROID_UIAUTOMATOR strategy!")
        value = f'UiScrollable(scrollable(true).instance(0)).scrollIntoView({value})'
        ui_automator = by, value
        self._driver.find_element(*ui_automator)
        y = self._driver.find_element(*ui_automator).rect['y']
        height = self._driver.get_window_size()["height"]
        if y > int(height * 3 / 4):
            self.swipe('down')
        if int(height / 4) > y:
            self.swipe('up')

    def scroll_to(self, direction: Literal["top", "bottom", "forward", "backward"],
                  operation: Literal["scroll", "fling"] = "scroll"):
        """
        only for android platform
        """
        directions = {"top": "ToBeginning(10)", "bottom": "ToEnd(10)",
                      "forward": "Forward()", "backward": "Backward()"}
        direction = directions.get(direction, None)
        if not direction:
            msg = f"{inspect.stack()[0][3]}('{direction}') only support the following params: {list(directions.keys())}!"
            raise IllegalArgumentException(msg)
        if operation not in ["scroll", "fling"]:
            msg = f"{inspect.stack()[0][3]}('{operation}') only support the following params: ['scroll', 'fling']!"
            raise IllegalArgumentException(msg)
        operation_selector = f'new UiScrollable(new UiSelector().scrollable(true)).{operation}{direction}'
        self._driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, operation_selector)

    @classmethod
    def wait(cls, seconds=5):
        time.sleep(seconds)

