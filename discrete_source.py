#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import os
import json
import random

# заимствовано из:
# https://github.com/joeyespo/py-getch/blob/master/getch/getch.py
try:
    from msvcrt import getch
except ImportError:
    def getch():
        """
        Gets a single character from STDIO.
        """
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

class DiscreteSource:
    data = {}
    N = 0
    event_list = list()
    is_infinite_process = False
    is_with_memory_source = False

    def __init__(self, argv):
        with open(argv[1], "r", encoding="utf-8") as read_file:
            self.data = json.load(read_file)
        if (argv[2] == "None"):
            self.is_infinite_process = True
        elif (int(argv[2]) <= 0):
            self.is_infinite_process = True
        else:
            self.is_infinite_process = False
            self.N = int(argv[2])
        i = 3
        while i < len(argv):
            self.event_list.append(int(argv[i]))
            i = i + 1
        print("len = ",len(self.data['switches']['switch_0']))
        if (len(self.data['switches']['switch_0']) > 1):
            self.is_with_memory_source = True
        else:
            self.is_with_memory_source = False

    def IsSourceWithMemory(self):
        return self.is_with_memory_source

    def GetEventList(self):
        return self.event_list

    def GetN(self):
        return self.N

    def ChooseObject(self, dict_to_choose, prob):
        bound_sum = 0
        for line in dict_to_choose:
            fract_dict = dict_to_choose[line].split("/")
            if (len(fract_dict) > 1):
                fract = float(fract_dict[0]) / float(fract_dict[1])
            else:
                fract = float(fract_dict[0])
            bound_sum = bound_sum + fract
            if (prob < bound_sum):
                return line

    def TransitionFunc(self, counter, in_symbol):
        if (self.event_list[counter] == in_symbol):
            return counter + 1
        else:
            if (counter > 0):
                i = 1
                while i <= counter:
                    sub_list = list(self.event_list[i : counter])
                    sub_list.append(in_symbol)
                    if (sub_list == self.event_list[0 : len(sub_list)]):
                        return len(sub_list)
                    i = i + 1
            return 0

    def InfiniteProcessWithoutMemory(self):
        child_pid = os.fork()
        if (child_pid > 0):
            # This is the parent process
            key = getch()
            while key != 'q':
                key = getch()
            os.kill(child_pid, 9)
        else:
            # This is the child process
            sum_meet = 0
            while True:
                j = 0
                while j < len(self.data['source']):
                    line1 = self.data['source'][j]
                    prob_coin = random.random()
                    coin = self.ChooseObject(self.data['switches'][line1][0], prob_coin)
                    prob_result = random.random()
                    result = self.ChooseObject(self.data['models'][coin][0], prob_result)
                    print(result, end = ' ')
                    j = j + 1
            print("\n", end = '')
            return

    def InfiniteProcessWithMemory(self):
        child_pid = os.fork()
        if (child_pid > 0):
            # This is the parent process
            key = getch()
            while key != 'q':
                key = getch()
            os.kill(child_pid, 9)
        else:
            # This is the child process
            state = self.data['source'][0]
            while True:
                coin_prob = random.random()
                coin = self.ChooseObject(self.data['switches'][state][0], coin_prob)
                prob_result = random.random()
                result = self.ChooseObject(self.data['models'][coin][0], prob_result)
                print(result, end = ' ')
                next_state_prob = random.random()
                state = self.ChooseObject(self.data['switches'][state][1], next_state_prob)
            print("\n", end = '')
            return

    def ProcessWithoutMemory(self):
        print("ProcessWithoutMemory:")
        if (self.is_infinite_process):
            self.InfiniteProcessWithoutMemory()
            return -1
        sum_meet = 0
        i = 0
        counter = 0
        while i < self.N:
            j = 0
            while (j < len(self.data['source'])) and (i + j < self.N):
                line1 = self.data['source'][j]
                prob_coin = random.random()
                coin = self.ChooseObject(self.data['switches'][line1][0], prob_coin)
                prob_result = random.random()
                result = self.ChooseObject(self.data['models'][coin][0], prob_result)
                if (len(self.event_list) > 0):
                    counter = self.TransitionFunc(counter, int(result))
                    if (counter == len(self.event_list)):
                        sum_meet = sum_meet + 1
                        counter = 0
                print(result, end = ' ')
                j = j + 1
            i = i + j
        print("\n", end = '')
        return sum_meet

    def ProcessWithMemory(self):
        print("ProcessWithMemory:")
        if (self.is_infinite_process):
            self.InfiniteProcessWithMemory()
            return -1
        sum_meet = 0
        state = self.data['source'][0]
        counter = 0
        sum_meet = 0
        for i in range(0, self.N):
            coin_prob = random.random()
            coin = self.ChooseObject(self.data['switches'][state][0], coin_prob)
            prob_result = random.random()
            result = self.ChooseObject(self.data['models'][coin][0], prob_result)
            if (len(self.event_list) > 0):
                    counter = self.TransitionFunc(counter, int(result))
                    if (counter == len(self.event_list)):
                        sum_meet = sum_meet + 1
                        counter = 0
            print(result, end = ' ')
            next_state_prob = random.random()
            state = self.ChooseObject(self.data['switches'][state][1], next_state_prob)
        print("\n", end = '')
        return sum_meet
