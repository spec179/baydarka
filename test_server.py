from __future__ import print_function

from concurrent import futures
import logging

import grpc
import raft_pb2
import raft_pb2_grpc

import asyncio


class Serv(raft_pb2_grpc.RaftServerServicer):
    def __init__(self) -> None:
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
            
    
async def main():
    task1 = asyncio.create_task(serve())
    task2 = asyncio.create_task(run())
    await task2
    await task1


async def serve():
    logging.basicConfig()
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_pb2_grpc.add_RaftServerServicer_to_server(Serv(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    await asyncio.sleep(5)
    server.wait_for_termination()


async def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    # print("Will try to greet world ...")
    # with grpc.insecure_channel('localhost:50051') as channel:
    #     stub = raft_pb2_grpc.RaftServerStub(channel)
    #     response = stub.RequestVote(raft_pb2.VoteRequest(id=1, term=1))
    #     print(response)
        #response2 = stub.RequestVote(raft_pb2.VoteRequest(id=2, term=2))
        #print('nice: ', response2.voteGranted)
    
    while True:
        print('abbaabababababa')
        await asyncio.sleep(3)


if __name__ == '__main__':
    asyncio.run(main())