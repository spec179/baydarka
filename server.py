from concurrent import futures

from common_data import *


class RaftServer(raft_server_pb2_grpc.RaftServerServicer):
    def __init__(self, parent):
        self.parent = parent

    def UpdateTerm(self, term):
        '''Обновление терма. Сервер становится фолловером'''
        self.parent.currentTerm = term
        self.parent.state = FOLLOWER
        self.parent.votedFor = None
        self.parent.timeout = random_timeout()
        logging.info(f"Server {self.parent.selfID} updated its term to {term}\n")

    def RequestVote(self, request, context):
        '''Реакция на VoteRequest. Метод Servicer.
        Условия положительного голоса:
        - терм не меньше, чем у голосующего;
        - лог не меньше, чем у голосующего; (AppendEntries пока не реализован)
        - этот сервер ещё не голосовал в этом терме.
        Если терм сервера меньше терма кандидата, он обновляет его и становится фолловером'''
        try:
            self.startTime = time.time()
            if request.term > self.parent.currentTerm:
                self.UpdateTerm(request.term)
            grantVote = request.term == self.parent.currentTerm and request.lastLogIndex >= len(self.parent.log) \
                        and self.parent.votedFor is None
            self.parent.votedFor = request.candidateID
            if grantVote:
                logging.info(f"Node {self.parent.selfID} voted for {request.candidateID}\n")
            else:
                logging.info(f"Node {self.parent.selfID} rejected VoteRequest from node {request.candidateID}\n")
            return raft_server_pb2.VoteReply(term=self.parent.currentTerm, voteGranted=grantVote)
        except Exception as e:
            print(traceback.format_exc())

    def serve(self):
        '''Запуск сервера как ответчика'''
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        raft_server_pb2_grpc.add_RaftServerServicer_to_server(self, server)
        server.add_insecure_port(ADD_ADDRESS.format(self.parent.selfID))
        server.start()
        server.wait_for_termination()
