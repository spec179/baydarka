from server import *
from client import *

'''Время работы программы'''
WAIT = 0.1


class RaftNode:
    def __init__(self, self_id):
        self.state = FOLLOWER
        self.currentTerm = 0
        self.selfID = self_id
        self.timeout = random_timeout()
        self.startTime = time.time()
        self.votedFor = None
        self.votes = 0
        self.log = []


def submit_server(server: RaftServer):
    '''Запуск сервера'''
    logging.info(f"Submitting server {server.parent.selfID}")
    server.serve()


def submit_client(client: RaftClient):
    '''Запуск клиента'''
    logging.info(f"Submitting client {client.parent.selfID}")
    client.run()


def runAllTemplate(selfID: int):
    '''Запуск узла: сервер и клиент одновременно'''
    logging.basicConfig()
    node = RaftNode(selfID)
    server = RaftServer(node)
    client = RaftClient(node)
    with futures.ThreadPoolExecutor(max_workers=2) as execRunServe:
        execRunServe.submit(lambda: submit_server(server))
        execRunServe.submit(lambda: submit_client(client))


"""
def terminate():
    '''Прекратить работу через определённое время, чтобы можно было проверить лог'''
    time.sleep(WAIT)
    quit()
"""


def runAllServers():
    '''Запуск всех серверов'''
    with futures.ThreadPoolExecutor(max_workers=NETWORK_SIZE) as execServers:
        for i in range(1, NETWORK_SIZE + 1):
            execServers.submit(lambda: runAllTemplate(i))
        # execServers.submit(terminate)


if __name__ == "__main__":
    logging.basicConfig(filename='raft.log', level=logging.DEBUG)
    runAllServers()
