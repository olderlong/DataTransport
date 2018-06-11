#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import time
import threading
from server import STATE_UPDATE_INTERVAL, AgentState
from common import event_manager, EVENT_HEARTBEAT


class AgentStateManager(object):
    def __init__(self):
        self.agent_state_dict = dict()
        self.__running = threading.Event()
        self.__state_monitor_thread = threading.Thread(target=self.__agents_state_monitor)

        event_manager.AddEventListener(EVENT_HEARTBEAT, self.add_new_agent)

    def add_new_agent(self, event):
        state_data = event.dict
        agent_state = AgentState()
        agent_state.gen_from_json_obj(state_data)
        self.update_agent_state(agent_state)

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
                        self.update_agent_state(agent_state)


            time.sleep(5)

    def __check_state(self, agent_state):
        lasttime = time.time() - agent_state.timestamp
        if lasttime > STATE_UPDATE_INTERVAL * 5.0 and lasttime <=STATE_UPDATE_INTERVAL * 10.0:
            return "Offline"
        elif lasttime > STATE_UPDATE_INTERVAL * 10.0:
            return "Dead"
        else:
            return "Online"


