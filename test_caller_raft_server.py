from __future__ import print_function

import logging

import grpc
import raft_pb2
import raft_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = raft_pb2_grpc.RaftServerStub(channel)
        response = stub.RequestVote(raft_pb2.VoteRequest(id=1, term=1))
        print(response)
        #response2 = stub.RequestVote(raft_pb2.VoteRequest(id=2, term=2))
        #print('nice: ', response2.voteGranted)


if __name__ == '__main__':
    logging.basicConfig()
    run()
