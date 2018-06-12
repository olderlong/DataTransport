#! /usr/bin/env python
# _*_ coding:utf-8 _*_
from agent import WVSControlBase

class AppScanControl(WVSControlBase):
    def __init__(self):
        agent_event = CommonEvent()
        event_manager.add_event_listener(agent_event.event_wvs_command, self.wvs_command_handler)

        self.wvs_action = "StartNewScan"

    def wvs_command_handler(self, event):
        command = event.dict
        print(str(command))

    def start_new_scan(self, config):
        pass

    def stop_scan(self):
        pass