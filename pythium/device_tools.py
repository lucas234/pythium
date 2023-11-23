# -*- coding: UTF-8 -*-
# @Project: pyium
# @File: device_tools
# @Author：Lucas Liu
# @Time: 2023/11/21 14:41
# @Software: PyCharm
import subprocess
import os
import dotenv
from pathlib import Path


class DeviceTools:

    @staticmethod
    def get_android_devices(adb_path=None, flag=""):
        """
        获取Android设备serial
        flag: -e 表示只获取emulator；-d 表示只获取真机；默认获取所有
        """
        devices = []
        if not adb_path:
            # for mac
            config_files = ['.bash_profile', '.bashrc', '.zshrc']
            path = Path("~").expanduser()
            android_homes = []
            for i in config_files:
                dotenv.load_dotenv(path.joinpath(i))
                android_home = os.getenv('ANDROID_HOME', None)
                if android_home:
                    android_homes.append(android_home)
            if android_homes:
                adb_path = Path(android_homes[0]).joinpath("platform-tools", "adb")
        output = subprocess.run(f'{adb_path} {flag} devices', capture_output=True, text=True, shell=True)
        lines = output.stdout.splitlines()
        stderr_ = output.stderr
        if output.returncode == 127:
            raise Exception('Please make sure ANDROID_HOME was set in system environment variables!')
        for line in lines[1:-1]:
            device = line.split('\t')[0].strip()
            devices.append(device)
        if not devices:
            raise Exception('No device found, please make sure your devices connected or emulators started')
        return devices

    @staticmethod
    def get_ios_devices():
        """get ios real devices"""
        devices = []
        output = os.popen('which idevice_id')
        lines = output.readlines()
        if len(lines) > 0:
            cmd = f'{lines[0].strip()} -l'
        else:
            cmd = '/usr/local/bin/idevice_id -l'
        output = os.popen(cmd)
        lines = output.readlines()
        for line in lines:
            device = line.strip()
            devices.append(device)
        return devices

    @staticmethod
    def get_ios_simulators():
        """get ios simulators"""
        devices = []
        output = os.popen('xcrun simctl list | grep Booted')
        lines = output.readlines()
        for line in lines:
            devices.append(line.split('(')[1].split(')')[0])
        return devices

    @staticmethod
    def is_port_idle(port_number):
        output = os.popen(f'lsof -i:{str(port_number)} | grep LISTEN')
        lines = output.readlines()
        return len(lines) == 0


if __name__ == '__main__':
    print(DeviceTools.get_ios_devices())
    # print(DeviceTools.get_ios_simulators())
    # print(DeviceTools.get_android_devices())

