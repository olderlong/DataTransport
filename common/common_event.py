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

        self.EVENT_WVS_STATE_RECV = "WVSStateRecv"
        self.event_wvs_state_recv = Event(type_=self.EVENT_WVS_STATE_RECV)

        self.EVENT_WVS_RESULT_RECV = "ScanResultRecv"
        self.event_scan_result_recv = Event(type_=self.EVENT_WVS_RESULT_RECV)

        self.EVENT_WVS_COMMAND = "WVSCommand"
        self.event_wvs_command = Event(type_=self.EVENT_WVS_COMMAND)

        self.EVENT_SERVER_COMMAND = "ServerCommand"
        self.event_server_command = Event(type_=self.EVENT_SERVER_COMMAND)
        self.EVENT_AGENT_EXIT = "AgentExit"
        self.event_agent_exit = Event(type_=self.EVENT_AGENT_EXIT)

        self.EVENT_SCAN_RESULT_SEND = "SendResultSend"
        self.event_scan_result_send = Event(type_=self.EVENT_SCAN_RESULT_SEND)

