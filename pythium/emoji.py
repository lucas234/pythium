# -*- coding: UTF-8 -*-
# @File: emoji
# @Author：Lucas Liu
# @Time: 2022/8/26 3:28 PM
# @Software: PyCharm


class Emoji(object):

    # http://www.unicode.org/emoji/charts/full-emoji-list.html
    # https://carpedm20.github.io/emoji/all.html?enableList=enable_list_alias&query=time
    PAUSE = '\u23f8\ufe0f'
    STOP = '\u23f9\ufe0f'
    EXCEPTION = '\U0001f6d1'
    FIND_LEFT = '\U0001F50D'
    FIND_RIGHT = '\U0001F50E'
    LINK = '\U0001f517'
    QUESTION = '\U00002753'
    CHECK_MARK_BUTTON = '\U00002705'
    CROSS_MARK_BUTTON = '\U0000274E'
    CROSS_MARK = '\U0000274C'
    HOURGLASS_DONE = '\U0000231B'
    HOURGLASS_NOT_DONE = '\U000023F3'
    # TIME: '\U000023F0', '\U000023F1', '\U0001F570'
    TIMEOUT = '\U000023F0'
    # BUG: '\U0001F41B', '\U0001F41E'
    BUG = '\U0001F41B'
    # WARNING: '\u26a0\ufe0f', '\U00002757'
    WARNING = '\u26a0\ufe0f'
    # KEYBOARD: '\u2328\ufe0f', '\U0001F3B9'
    KEYBOARD = '\u2328\ufe0f'
    FORWARD = '\u27a1\ufe0f'
    # BACK: '\U0001f519', '\u2b05\ufe0f'
    BACK = '\U0001f519'
    OFF = '\U0001f4f4'
    TEXT = '\U0001f4d6'
    RUN = '\U0001F7E2'


if __name__ == '__main__':
    print(f"{Emoji.CHECK_MARK_BUTTON} Find")
    print(f"{Emoji.CROSS_MARK} Find")
    print('\U00002402,\U00002403 Find')
    print("🚧")
    print("\U0001f4dd")
