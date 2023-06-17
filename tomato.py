#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Pomodoro 番茄工作法 https://en.wikipedia.org/wiki/Pomodoro_Technique
# ====== 🍅 Tomato Clock =======
# ./tomato.py         # start a 25 minutes tomato clock + 5 minutes break
# ./tomato.py -t      # start a 25 minutes tomato clock
# ./tomato.py -t <n>  # start a <n> minutes tomato clock
# ./tomato.py -b      # take a 5 minutes break
# ./tomato.py -b <n>  # take a <n> minutes break
# ./tomato.py -h      # help


import sys
import time
import subprocess
import beepy
import random

WORK_MINUTES = 25
BREAK_MINUTES = 5
LONG_BREAK_MINUTES = 15
TOMATOS = 4


def main():

    try:
        if len(sys.argv) <= 1:
            tomato(WORK_MINUTES, BREAK_MINUTES, TOMATOS)

        elif len(sys.argv) == 3 and sys.argv[1] == '-t':
            minutes = int(sys.argv[2])
            tomato(minutes, BREAK_MINUTES, TOMATOS)

        elif len(sys.argv) == 3 and sys.argv[1] == '-b':
            minutes = int(sys.argv[2])
            tomato(WORK_MINUTES, minutes, TOMATOS)

        elif len(sys.argv) == 5:
            work_minutes = int(sys.argv[2])
            break_minutes = int(sys.argv[4])
            tomato(work_minutes, break_minutes, TOMATOS)

        elif sys.argv[1] == '-h':
            help()

        else:
            help()

    except KeyboardInterrupt:
        print('\n👋 goodbye')
    except Exception as ex:
        print(ex)
        exit(1)


def tomato(work_minutes, break_minutes, tomatos):
    for tomato in range(TOMATOS):
        print('\r\r', f'{"🍅" * (tomato+1)}/{"🍅" * tomatos} Ctrl+C to exit')
        countdown(work_minutes)
        notify_me("It is time to take a break")
        countdown(break_minutes)
        notify_me("It is time to work")

def countdown(minutes):
    start_time = time.perf_counter()
    while True:
        diff_seconds = int(round(time.perf_counter() - start_time))
        left_seconds = minutes * 60 - diff_seconds
        if left_seconds <= 0:
            print('')
            break

        countdown = '{}:{} ⏰'.format(int(left_seconds / 60), int(left_seconds % 60))
        duration = min(minutes, 25)
        progressbar(diff_seconds, minutes * 60, duration, countdown)
        time.sleep(1)


def progressbar(curr, total, duration=10, extra=''):
    frac = curr / total
    filled = round(frac * duration)
    print('\r', '🍅' * filled + '--' * (duration - filled), '[{:.0%}]'.format(frac), extra, end='')


def notify_me(msg):
    '''
    # macos desktop notification
    terminal-notifier -> https://github.com/julienXX/terminal-notifier#download
    terminal-notifier -message <msg>

    # ubuntu desktop notification
    notify-send

    # voice notification
    say -v <lang> <msg>
    lang options:
    - Daniel:       British English
    - Ting-Ting:    Mandarin
    - Sin-ji:       Cantonese
    '''

    print(msg)
    try:
        if sys.platform == 'darwin':
            # macos desktop notification
            subprocess.run(['terminal-notifier', '-title', '🍅', '-message', msg])
            subprocess.run(['say', '-v', 'Daniel', msg])
        elif sys.platform.startswith('linux'):
            # ubuntu desktop notification
            subprocess.Popen(["notify-send", '🍅', msg])
            beepy.beep(random.randint(1, 7))
        else:
            # windows?
            # TODO: windows notification
            pass

    except:
        # skip the notification error
        pass


def help():
    appname = sys.argv[0]
    appname = appname if appname.endswith('.py') else 'tomato'  # tomato is pypi package
    print('====== 🍅 Tomato Clock =======')
    print(f'{appname} -t <n>  # start a <n> minutes tomato clock')
    print(f'{appname} -b <n>  # start a tomato clock with <n> minutes break')
    print(f"{appname} -t <n> -b <m>  # start a <n> minutes tomato clock with <m> minutes break")
    print(f'{appname} -h      # help')


if __name__ == "__main__":
    main()
