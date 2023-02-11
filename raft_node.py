from concurrent.futures import *
from threading import Lock
import grpc
import raft_pb2_grpc
from raft_client import Client
from raft_server import Server


def start_server(server):
    grpc_server = grpc.server(ThreadPoolExecutor(max_workers=10))
    raft_pb2_grpc.add_ServerServicer_to_server(server, grpc_server)
    grpc_server.add_insecure_port('localhost:50051')
    grpc_server.start()
    grpc_server.wait_for_termination()


def start_client(client):
    try:
        client.term()
    except Exception as error:
        print(error)


class Node:
    id = 0
    status = 0
    term = 0
    votedFor = None
    log = []
    commitIndex = 0
    lastAplied = 0
    lock = Lock()

    def __init__(self):
        self.executor = ThreadPoolExecutor()
        self.server = Server(self)
        self.client = Client(self)

        server_f = self.executor.submit(start_server, self.server)
        client_f = self.executor.submit(start_client, self.client)


if __name__ == "__main__":
    node = Node()