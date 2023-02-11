import grpc
import raft_pb2_grpc
import raft_pb2
import asyncio
import time


class Client:
    def __init__(self, parent):
        self.parent = parent
        channels = [grpc.insecure_channel('localhost:50052')]
        self.stubs = [raft_pb2_grpc.ServerStub(channel) for channel in channels]

    def term(self):
        while True:
            if self.parent.status == 0:
                time.sleep(2)
            print(1)
            self.parent.lock.acquire()
            self.parent.term += 1
            self.parent.status = 1
            self.parent.votedFor = self.parent.id
            self.parent.lock.release()
            self.election()

    async def vote(self, stub):
        result = stub.GetVote(
            raft_pb2.Candidate(term=self.parent.term, candidateId=self.parent.id, lastLogId=0, lastLogTerm=0))
        return result

    def election(self):
        voted = 1
        term = self.parent.term
        for stub in self.stubs:
            task = asyncio.run(self.vote(stub))
            asyncio.sleep(1)
            task.close()
            if task.result:
                if task.result.voteGranted:
                    voted += 1
                else:
                    self.parent.lock.acquire()
                    self.status = 0
                    self.parent.lock.release()
            if voted >= 1:
                if self.parent.term > term:
                    self.parent.lock.acquire()
                    self.status = 0
                    self.parent.lock.release()
                else:
                    self.parent.lock.acquire()
                    self.status = 2
                    self.parent.lock.release()
