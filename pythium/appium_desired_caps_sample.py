import platform
import re
from pathlib import Path
import os


class AppiumDesiredCapsSample:

    @staticmethod
    def get_app_package_activity(aapt_path, package_path):
        # aapt 在android-sdk下的build-tools中，使用前确保环境变量已经设置
        # example: /usr/local/Caskroom/android-sdk/4333796/build-tools/29.0.2
        command_type = "grep" if platform.system() in ['Darwin', 'Linux'] else "findstr"
        command = f"{Path(aapt_path).joinpath('aapt')} dump badging {package_path} | {command_type} "
        pattern = re.compile(r"name='(.*?)'")
        app_package = pattern.findall(os.popen(command + "package").read())[0]
        app_activity = pattern.findall(os.popen(command + "launchable-activity").read())[0]
        print(f"the app app_package and app_activity is: {app_package}, {app_activity}.")
        return app_package, app_activity

    @staticmethod
    def get_ios_dc(is_simulator=False):
        simulator_desired_caps = {
            "platformName": 'iOS',
            "platformVersion": '14.5',
            "automationName": 'XCUITest',  # xcuitest
            "deviceName": 'iPhone 12 Pro',
            "noReset": True,
            "connectHardwareKeyboard": True,
            "udid": 'B49289C1-2221-4BC5-94DD-963C6827A425',
            "app": "/Users/xxx/Downloads/Payload/xxx.app"
        }

        real_desired_caps = {
            "appium:platformVersion": "14.2",
            "appium:deviceName": "iPhone 8",
            "appium:udid": "d3268cdf257a8abb0729fa2031435f17d4b6e234",
            "appium:noReset": True,
            "platformName": "iOS",
            "appium:automationName": "XCUITest",
            "appium:app": "/Users/xxx/Downloads/xxx.ipa",
            "appium:xcodeOrgId": "QN7T73D23",
            "appium:xcodeSigningId": "google LLC"
        }
        return simulator_desired_caps if is_simulator else real_desired_caps

    @staticmethod
    def get_android_dc(is_emulator=False):
        emulator_desired_caps = {'platformName': 'Android', 'platformVersion': '9.0', 'automationName': 'uiautomator2',
                                 'deviceName': 'emulator-5554', 'noReset': True,
                                 'app': '/Users/xxx/Downloads/xxx-debug.apk'}
        real_desired_caps = {'platformName': 'Android', 'platformVersion': '10', 'automationName': 'uiautomator2',
                             'deviceName': '45722ede', 'noReset': True,
                             'app': '/Users/xxx/Downloads/xxx-debug.apk', 'appPackage': 'com.xxx',
                             'appActivity': 'com.xxx.mobile.product.splash.view.SplashActivity'}
        return emulator_desired_caps if is_emulator else real_desired_caps


if __name__ == '__main__':
    print(AppiumDesiredCapsSample.get_android_dc())
    print(AppiumDesiredCapsSample.get_ios_dc())
