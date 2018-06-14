#! /usr/bin/env python
# _*_ coding:utf-8 _*_

import time
import threading
from server import CCServer, AgentStateMonitor
from common import event_manager, agent_event

server = CCServer()
agent_state_monitor = AgentStateMonitor()

command = {
    "Type": "WVSCommand",
    "Data": {
        "Action": "StartNewScan",
        "Config": {  # 可选，当命令为StartNewScan时需提供该字段作为扫描参数
            "StartURL": "http://www.cnblog.com",
            "ScanPolicy": "Normal"
        }
    }
}
exit_agent = {
    "Type": "AgentControl",
    "Data": {
        "Control": "Exit"
    }
}


def command_start_scan(server, command_json):
    for index in range(3):
        # server.send_command(command_json)
        agent_event.event_server_command.dict = command_json
        # print("in run_server " + str(agent_event.event_wvs_command.dict))
        event_manager.send_event(agent_event.event_server_command)
        time.sleep(3)
    # command_exit_agent(exit_agent)


def command_exit_agent(command_json):
    # server.send_command(command_json)
    agent_event.event_server_command.dict = command_json
    event_manager.send_event(agent_event.event_server_command)


def server_run():
    server.start()
    agent_state_monitor.start_monitor()

    time.sleep(10)
    th = threading.Thread(target=command_start_scan, args=(server, command))
    th.daemon = True
    th.start()


def server_stop():
    print("server stop...")
    server.stop()
    agent_state_monitor.stop_monitor()
    event_manager.stop()


if __name__ == '__main__':
    server_run()

    time.sleep(50)
    server_stop()
