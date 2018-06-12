import cli_app.run_agent as agent
import cli_app.run_server as server
import threading
import time


def run():
    server.server_run()
    agent.agent_run()


def main():
    server_thread = threading.Thread(target=server.server_run)
    server_thread.start()
    agent_thread = threading.Thread(target=agent.agent_run)
    agent_thread.start()
    server_thread.join()
    agent_thread.join()


if __name__ == '__main__':
    main()
    # run()
    time.sleep(50)
