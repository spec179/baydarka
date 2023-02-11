import grpc
import raft_pb2
import raft_pb2_grpc


class Server(raft_pb2_grpc.ServerServicer):
    def __init__(self, parent):
        self.parent = parent

    def GetVote(self, request, context):
        if (not self.parent.votedFor or self.parent.votedFor == request.candidateId) \
                and self.parent.term <= request.term:
            self.parent.lock.acquire()
            if self.parent.term < request.term:
                self.parent.status = 0
            self.parent.term = request.term
            self.parent.votedFor = request.candidateId
            self.parent.lock.release()
            return raft_pb2.Vote(term=self.parent.term, voteGranted=True)
        else:
            return raft_pb2.Vote(term=self.parent.term, voteGranted=False)
