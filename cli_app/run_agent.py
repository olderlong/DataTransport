#! /usr/bin/env python
# _*_ coding:utf-8 _*_

from agent import CCAgent, AppScanControl
from common import agent_event, event_manager

agent = CCAgent(name="AppScan", port=5555, cc_server_address=("192.168.195.1", 6666))
appscan = AppScanControl()


def agent_run():
    print("Agent running...")
    agent.start()


def agent_stop(event):
    # print(event.dict)
    print("agent exit...")
    appscan.stop_scan()
    agent.stop()
    event_manager.stop()


event_manager.add_event_listener(agent_event.EVENT_AGENT_EXIT, agent_stop)

if __name__ == '__main__':

    agent_run()
