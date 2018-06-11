#! /usr/bin/env python
# _*_ coding:utf-8 _*_

from common import CommonEvent, event_manager


class WVSControlBase(object):
    def __init__(self):
        agent_event = CommonEvent()
        event_manager.add_event_listener(agent_event.event_wvs_command, self.wvs_command_handler)

        self.wvs_action = "StartNewScan"
        self.scan_config = {}

    def wvs_command_handler(self, event):
        command_pkg = event.dict
        print(str(command_pkg))

    def start_new_scan(self, config):
        pass

    def stop_scan(self):
        pass