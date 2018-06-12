#! /usr/bin/env python
# _*_ coding:utf-8 _*_

# from data_transport import *
# # from data_transport.event_manager import event_manager
# # from data_transport.cc_server import EVENT_HEARTBEAT
import time
import threading
from agent import CCAgent, AppScanControl
from common import event_manager
from server import CCServer, AgentStateMonitor


def send_command(server, json_msg):
    command = {
        "Type":"WVSCommand",
        "Data":{
            "Action": "StartNewScan",
            "Config": { # 可选，当命令为StartNewScan时需提供该字段作为扫描参数
                "StartURL": "http://www.cnblog.com",
                "ScanPolicy": "Normal"
            }
        }
    }
    for index in range(3):
        server.send_command(command)
        # agent.send_json_to(json_msg, server.address)
        # time.sleep(0.5)
        # server.send_msg_to("Hello world# {} ".format(index), agent.address)
        time.sleep(1)


if __name__ == '__main__':
    json_msg = {"name":"Angares","age":18}
    server = CCServer()
    agent = CCAgent(name="Agent_1", cc_server_address=server.address)
    server.start()
    agent.start()
    # ll = Listener("aa")

    # event_manager.start()
    agent_state_monitor = AgentStateMonitor()
    agent_state_monitor.start_monitor()

    # event_manager.Start()
    # agent.start_heartbeat(2)

    # agent_1 = CCAgent(cc_server_address=server.address, port=5556, name="Agent_2")
    # agent_1.start()
    appscan = AppScanControl()
    # agent_1.start_heartbeat(2)

    th = threading.Thread(target=send_command, args=(server, json_msg))
    th.daemon = True
    th.start()
    # th.join()


    time.sleep(20)
    agent.stop()
    # t.join()
    time.sleep(60)


    # agent_1.stop()
    # agent.stop()
    server.stop()
    agent_state_monitor.stop_monitor()
    event_manager.stop()

