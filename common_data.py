'''Константы и утилитарные функции для использования программой'''

import grpc
import raft_server_pb2
import raft_server_pb2_grpc

import random
import time
import sys
import traceback
import logging


'''Состояния сервера'''
LEADER = 0
FOLLOWER = 1
CANDIDATE = 2

'''Нижняя и верхняя граница возможного таймаута сервера, а также ритм лидера'''
MIN_TIMEOUT = 150
MAX_TIMEOUT = 300
HEARTBEAT = 30

'''Шаблоны используемых адресов'''
OPEN_ADDRESS = "localhost:5005{}"
ADD_ADDRESS = "[::]:5005{}"


def random_timeout():
    '''Генерация случайного времени таймаута'''
    return random.randrange(MIN_TIMEOUT, MAX_TIMEOUT, HEARTBEAT) / 1000
