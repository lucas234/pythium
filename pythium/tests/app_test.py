# -*- coding: UTF-8 -*-
# @Project: CodeWarehouse
# @File: example
# @Author：Lucas Liu
# @Time: 2022/1/18 4:26 下午
# @Software: PyCharm
from appium import webdriver
from pythium import Falcon, Element, Page
from appium.webdriver.webdriver import AppiumBy, By


android_desired_caps = dict(
    platformName='Android',
    platformVersion='9.0',
    automationName='uiautomator2',
    deviceName='emulator-5554',
    noReset=True,
    app='/Users/bo.liu/Downloads/globalapp-debug.apk')
real_android_desired_caps = dict(
    platformName='Android',
    platformVersion='13',
    automationName='uiautomator2',
    deviceName='R5CWA0XWCSV',
    noReset=True,
    app='/Users/bo.liu/Downloads/0529.apk',
    appPackage="com.iherb",
    appActivity="com.iherb.mobile.product.splash.view.SplashActivity"
)
ios_desired_caps = {
    "platformName": 'iOS',
    "platformVersion": '14.5',
    "automationName": 'XCUITest',  # xcuitest
    "deviceName": 'iPhone 12 Pro',
    "noReset": True,
    "connectHardwareKeyboard": True,
    "udid": 'B49289C1-2221-4BC5-94DD-963C6827A425',
    "app": "/Users/bo.liu/Downloads/Payload/iHerb.app"
}

real_ios_desired_caps = {
  "appium:platformVersion": "",
  "appium:deviceName": "iOS device",
  "appium:udid": "00008110-000270D12E40A01E",
  "appium:noReset": True,
  "platformName": "iOS",
  "appium:automationName": "XCUITest",
  "appium:app": "/Users/bo.liu/Downloads/iHerb.ipa",
  "appium:xcodeOrgId": "24Y2VQTKE3",
  "appium:xcodeSigningId": "iPhone Developer"
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', real_ios_desired_caps)
Elem = Falcon(Element, driver)
page = Page(driver)
# driver.find_element(AppiumBy.ACCESSIBILITY_ID, "IHBPDPAutoshipAndSaveCompactView-$__lazy_storage_$_radioButton-7-0").click()
# Elem(android_uiautomator='resourceId("com.iherb:id/tv_sign_out")').scroll_into_view()
# Elem(android_uiautomator='resourceId("com.iherb:id/btn_ask_question")').scroll_into_view(swipe_max_times=3)
# Elem(ios_predicate='label == "Ask a question" AND name == "Ask a question"').scroll_into_view(swipe_max_times=10)
# Elem(accessibility_id='Ask a question').scroll_into_view(swipe_max_times=10)
Elem(accessibility_id='IHBPDPAutoshipAndSaveCompactView-$__lazy_storage_$_radioButton-7-0').scroll_into_view(swipe_max_times=3)
# driver.terminate_app("iHerb.iHerb")
# print("activate app")
# safari = "com.apple.mobilesafari"
# app = "iHerb.iHerb"
# driver.activate_app(f"{safari}")
# print(ios_desired_caps)
# bundle_id = driver.execute_script('mobile: activeAppInfo')
print(driver.execute_script('mobile: deviceInfo'))
# driver.get('https://secure.iherb.com/myaccount/subscription')
# driver.execute_script('mobile: terminateApp', {"bundleId": "iHerb.iHerb"})
# print(bundle_id)
# driver.terminate_app('iHerb.iHerb')
# driver.terminate_app('iHerb.iHerb')
