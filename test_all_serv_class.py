from threading import Lock

from concurrent import futures

import logging
import asyncio
import grpc
import raft_pb2
import raft_pb2_grpc

class Server(raft_pb2_grpc.RaftServerServicer):
    def __init__(self, parent) -> None:
        self.parent = parent
        super().__init__()
        self.term = 1
        self.hasVoted = False
    
    def RequestVote(self, request, context):
        if self.term > request.term:
            return raft_pb2.VoteReply(return_term=self.term, voteGranted=False)
        if self.hasVoted:
            return raft_pb2.VoteReply(voteGranted=False)
        else:
            print('HasVoted!!')
            self.term = request.term
            print("updated term: ", request.term)
            self.hasVoted = True
            return raft_pb2.VoteReply(voteGranted=True)
    
    async def serve(self):
        logging.basicConfig()
        port = '50051'
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        raft_pb2_grpc.add_RaftServerServicer_to_server(self, server)
        server.add_insecure_port('[::]:' + port)
        server.start()
        print("Server started, listening on " + port)
        await asyncio.sleep(5)
        server.wait_for_termination()
    

class Client():
    def __init__(self, parent) -> None:
        self.parent = parent
    
    def call():
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = raft_pb2_grpc.RaftServerStub(channel)
            response = stub.RequestVote(raft_pb2.VoteRequest(id=1, term=1))
            print(response)
        #response2 = stub.RequestVote(raft_pb2.VoteRequest(id=2, term=2))
        #print('nice: ', response2.voteGranted)


class Node():
    def __init__(self) -> None:
        self.state = 'follower'
        self.server = Server(parent=self)
        self.client = Client(parent=self)
        self.lock = Lock()
        logging.basicConfig()
    
    async def run(self):
        with futures.ThreadPoolExecutor(2) as executor:
            _1 = executor.submit(self.server.serve)
            await asyncio.sleep(8)
            _2 = executor.submit(print, 'ABOBAOBOABOBAOBABOBAA')


if __name__ == '__main__':
    node = Node()
    asyncio.run(node.run)