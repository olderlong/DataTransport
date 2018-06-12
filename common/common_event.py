#! /usr/bin/env python
# _*_ coding:utf-8 _*_
from common import Event


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@singleton
class CommonEvent(object):
    def __init__(self):
        self.EVENT_HEARTBEAT = "Heartbeat"
        self.event_heartbeat = Event(type_=self.EVENT_HEARTBEAT)
        self.EVENT_WVS_STATE = "WVSState"
        self.event_wvs_state = Event(type_=self.EVENT_WVS_STATE)
        self.EVENT_WVS_RESULT = "ScanResult"
        self.event_scan_result = Event(type_=self.EVENT_WVS_RESULT)

        self.EVENT_WVS_COMMAND = "WVSCommand"
        self.event_wvs_command = Event(type_=self.EVENT_WVS_COMMAND)
