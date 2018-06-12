#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import threading
# from server import STATE_UPDATE_INTERVAL, AgentState
from .agent_state import *
from common import event_manager, CommonEvent


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@singleton
class AgentStateMonitor(object):
    """
    代理状态监视类，为单例模式
    """
    def __init__(self):
        self.agent_state_dict = dict()
        self.__running = threading.Event()
        self.__state_monitor_thread = threading.Thread(target=self.__agents_state_monitor)
        agent_event = CommonEvent()
        event_manager.add_event_listener(agent_event.EVENT_HEARTBEAT, self.add_new_agent_state)

    def add_new_agent_state(self, event):
        state_data = event.dict
        agent_state = AgentState()
        agent_state.gen_from_json_obj(state_data)
        # self.update_agent_state(agent_state)
        self.agent_state_dict[agent_state.agent_identifier] = agent_state

    def update_agent_state(self, agent_state):
        self.agent_state_dict[agent_state.agent_identifier] = agent_state
        agent_state.print_state()

    def start_monitor(self):
        self.__running.set()
        self.__state_monitor_thread.daemon = True
        self.__state_monitor_thread.start()

    def stop_monitor(self):
        self.__running.clear()
        self.agent_state_dict.clear()

    def __agents_state_monitor(self):
        while self.__running:
            if len(self.agent_state_dict) > 0:
                for agent_state in list(self.agent_state_dict.values()):
                    new_state = self.__check_state(agent_state)
                    if new_state == "Dead":
                        print("Agent {0} is dead.\nAgent {1} is removed.".format(
                            agent_state.agent_identifier,
                            agent_state.agent_identifier))

                        self.agent_state_dict.pop(agent_state.agent_identifier)
                    else:
                        agent_state.state = new_state
                        agent_state.print_state()
                        self.agent_state_dict[agent_state.agent_identifier] = agent_state
                        # self.update_agent_state(agent_state)

            time.sleep(5)

    def __check_state(self, agent_state):
        """
        根据前后两次时标对比判断代理状态，时标间隔大于2倍更新时间小于3倍更新时间时为离线，更长时间为Dead
        :param agent_state: 代理状态对象
        :return: 代理状态：Offline、Dead、Online
        """
        last_time = time.time() - agent_state.timestamp
        if STATE_UPDATE_INTERVAL * 2.0 < last_time <= STATE_UPDATE_INTERVAL * 5.0:
            return "Offline"
        elif last_time > STATE_UPDATE_INTERVAL * 5.0:
            return "Dead"
        else:
            return "Online"


if __name__ == '__main__':
    monitor = AgentStateMonitor()
    print(id(monitor))
    monitor1 = AgentStateMonitor()
    print(id(monitor1))
