from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from appium.webdriver.webdriver import WebDriver as MobileDriver
from retrying import retry
from typing import Literal, Union
from loguru import logger
from pythium.utils import Utils
from pythium.actions import Actions
from pythium.assertions import ElemAssertions, ElemsAssertions
from pythium.emoji import Emoji


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
        self._action = Actions(self._driver)

    def __get__(self, obj, owner):
        """Gets the element object"""
        self._driver = obj.driver
        self._action = Actions(self._driver)
        # self.elems = self._find_elements()
        return self

    @property
    def elems(self):
        return self._find_elements()

    def _find_elements(self, timeout=_TIMEOUT):
        by, value = self._locator
        try:
            elem = WebDriverWait(self._driver, timeout).until(ec.presence_of_all_elements_located(self._locator))
            logger.info(f"{Emoji.FIND_LEFT} Find element: {by}='{value}'.")
            return elem
        except TimeoutException as te:
            logger.exception(te)
            elem = self._driver.find_elements(*self._locator)
            logger.info(f"{Emoji.FIND_LEFT} Find element: {by}='{value}'.")
            return elem
        except NoSuchElementException as nse:
            logger.exception(nse)
            elem = self._driver.find_elements(*self._locator)
            logger.info(f"{Emoji.FIND_LEFT} Find element: {by}='{value}'.")
            return elem

    @property
    def expect(self) -> ElemsAssertions:
        logger.info(f"{Emoji.ASSERT} Start to element assertions.")
        return ElemsAssertions(self)

    @property
    def count(self, timeout=_TIMEOUT):
        return len(self._find_elements(timeout))

    def index(self, n, timeout=_TIMEOUT):
        return self._find_elements(timeout)[n]

    def wait(self, seconds=5):
        self._action.wait(seconds)
        logger.info(f"{Emoji.HOURGLASS_NOT_DONE} wait {seconds}s")
        return self

    @property
    def texts(self, timeout=_TIMEOUT):
        elements = self._find_elements(timeout)
        if self._action.is_web_platform:
            texts = [elem.get_attribute('textContent') for elem in elements]
            logger.info(f"{Emoji.TEXT} texts: {texts}.")
            return texts
        if self._action.is_mobile_platform:
            texts = [elem.text for elem in elements]
            logger.info(f"{Emoji.TEXT} texts: {texts}.")
            return texts


class Element:

    _TIMEOUT = 8

    def __init__(self, id_=None, css=None, name=None, xpath=None, partial_link_text=None, link_text=None,
                 class_name=None, tag_name=None, image=None, custom=None, android_uiautomator=None,
                 android_viewtag=None, android_data_matcher=None, android_view_matcher=None,
                 windows_ui_automation=None, accessibility_id=None, ios_uiautomation=None, ios_class_chain=None,
                 ios_predicate=None, driver: Union[WebDriver, MobileDriver] = None):
        _locators = {k: v for k, v in Utils.get_kwargs().items() if v}
        if 'driver' in _locators:
            _locators.pop('driver')
        self._locator = Utils.valid_locator(_locators)[:2]
        self._driver = driver
        self._action = Actions(self._driver)

    def __get__(self, obj, owner):
        """Gets the element object"""
        self._driver = obj.driver
        self._action = Actions(self._driver)
        # self.elem = self._find_element()
        return self

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        self.__get__(obj, obj.__class__)
        self._find_element().clear()
        self._find_element().send_keys(value)

    @property
    def elem(self):
        return self._find_element()

    @property
    def expect(self) -> ElemAssertions:
        logger.info(f"{Emoji.ASSERT} Start to element assertions.")
        return ElemAssertions(self)

    def _find_element(self, timeout=_TIMEOUT):
        by, value = self._locator
        try:
            elem = WebDriverWait(self._driver, timeout).until(ec.presence_of_element_located(self._locator))
            logger.info(f"{Emoji.FIND_LEFT} Find element: {by}='{value}'.")
            self._action.highlight(elem)
            return elem
        except TimeoutException as te:
            logger.exception(te)
            elem = self._driver.find_element(*self._locator)
            logger.info(f"{Emoji.FIND_LEFT} Find element(timeout): {by}='{value}'.")
            self._action.highlight(elem)
            return elem
        except NoSuchElementException as nse:
            logger.exception(nse)
            elem = self._driver.find_element(*self._locator)
            logger.info(f"{Emoji.FIND_LEFT} Find element(no_such): {by}='{value}'.")
            self._action.highlight(elem)
            return elem

    def wait_until_visible(self, timeout=_TIMEOUT, throw_exception=True):
        self._action.wait_util(self._locator, ec.visibility_of_element_located, timeout, throw_exception)
        return self

    def wait_util_clickable(self, timeout=_TIMEOUT, throw_exception=True):
        self._action.wait_util(self._locator, ec.element_to_be_clickable, timeout, throw_exception)
        return self

    def wait_util_presence(self, timeout=_TIMEOUT, throw_exception=True):
        self._action.wait_util(self._locator, ec.presence_of_element_located, timeout, throw_exception)
        return self

    def wait(self, seconds=5):
        self._action.wait(seconds)
        return self

    def is_visible(self, timeout=_TIMEOUT):
        return self._action.is_(self._locator, ec.visibility_of_element_located, timeout)

    def is_in_view(self, top_offset=100, bottom_offset=100):
        return self._action.is_in_view(self._locator, top_offset, bottom_offset)

    def is_selected(self, timeout=_TIMEOUT):
        return self._action.is_(self._locator, ec.element_located_to_be_selected, timeout)

    def is_disappeared(self, timeout=_TIMEOUT):
        return self._action.is_(self._locator, ec.invisibility_of_element_located, timeout)

    def is_exist(self, timeout=_TIMEOUT):
        try:
            self._find_element(timeout)
            logger.info(f"{Emoji.CHECK_MARK_BUTTON} is_displayed().")
            return True
        except Exception as ex:
            by, value = self._locator
            logger.info(f"{Emoji.CROSS_MARK} element: by.{by}='{value}' is not exist! original exception: {ex}")
            return False

    def clear(self):
        self._find_element().clear()
        logger.info(f"{Emoji.CHECK_MARK_BUTTON} clear().")
        return self

    def click_if_exist(self, timeout=_TIMEOUT, by: Literal['js', 'default', 'action'] = 'default'):
        if self.is_exist(timeout):
            self.click(by)
        return self

    def hover(self, timeout=_TIMEOUT):
        self._action.action_chains.move_to_element(self._find_element(timeout)).perform()

    @retry(retry_on_exception=retry_if_exceptions, stop_max_attempt_number=2, wait_fixed=1000)
    def click(self, by: Literal['js', 'default', 'action', 'coordinate'] = 'default', timeout=_TIMEOUT):
        by = by.lower()
        if by == "js":
            # only support web
            if self._action.is_web_platform:
                self._driver.execute_script("arguments[0].click();", self._find_element(timeout))
                logger.info(f"{Emoji.MOUSE} click() by js.")
            else:
                raise Exception(f"Clicking element by js only support web platform.")
        elif by == 'action':
            self._action.action_chains.click(self._find_element(timeout)).perform()
            logger.info(f"{Emoji.MOUSE} click() by action.")
        elif by == 'coordinate':
            # only support mobile
            if self._action.is_web_platform:
                raise Exception(f"Clicking element by coordinate only support mobile platform.")
            location = self._find_element(timeout).location
            x = location['x']
            y = location['y']
            self._driver.tap([(x, y)])
            logger.info(f"{Emoji.MOUSE} click() by coordinate.")
        elif by == 'default':
            self._find_element().click()
            logger.info(f"{Emoji.MOUSE} click().")
        else:
            raise Exception(f"'by' only support the following strategies: ['js', 'default', 'action', 'coordinate']")
        return self

    def send_keys(self, value):
        self._find_element().send_keys(value)
        logger.info(f"{Emoji.KEYBOARD} send_keys('{value}').")
        return self

    def get_attribute(self, name):
        value = self._find_element().get_attribute(name)
        logger.info(f"{Emoji.CHECK_MARK_BUTTON} get_attribute('{name}') -> {value}.")
        return value

    def value_of_css_property(self, name):
        value = self._find_element().value_of_css_property(name)
        logger.info(f"{Emoji.CHECK_MARK_BUTTON} get_value_of_css_property('{name}') -> {value}.")
        return value

    def get_property(self, name):
        value = self._find_element().get_property(name)
        logger.info(f"{Emoji.CHECK_MARK_BUTTON} get_property('{name}') -> {value}.")
        return value

    @property
    def text(self):
        if self._action.is_web_platform:
            text = self._find_element().get_attribute('textContent')
            logger.info(f"{Emoji.TEXT} text: {text}.")
            return text
        if self._action.is_mobile_platform:
            text = self._find_element().text
            logger.info(f"{Emoji.TEXT} text: {text}.")
            return text

    def scroll_into_view(self, direction='down', swipe_max_times=5, top_offset=100, bottom_offset=100, timeout=_TIMEOUT):
        if self._action.is_web_platform:
            self._driver.execute_script("arguments[0].scrollIntoView(true);", self._find_element(timeout))
            logger.info(f"{Emoji.CHECK_MARK_BUTTON} scroll into view.")
        if self._action.is_mobile_platform:
            self._action.scroll_into_view(self._locator, direction, swipe_max_times, top_offset, bottom_offset)
            logger.info(f"{Emoji.RUN} scroll {direction} into view.")
        return self

    def switch_to_iframe(self, timeout=_TIMEOUT):
        WebDriverWait(self._driver, timeout).until(ec.frame_to_be_available_and_switch_to_it(self._locator))
        logger.info(f"{Emoji.CHECK_MARK_BUTTON} switch to iframe.")

    def switch_to_default_content(self):
        self._driver.switch_to.default_content()
        logger.info(f"{Emoji.CHECK_MARK_BUTTON} switch to default content.")
        return self

