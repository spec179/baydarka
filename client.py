from common_data import *


'''Количество серверов и нижняя граница большинства голосов'''
NETWORK_SIZE = 5
MAJORITY = (NETWORK_SIZE + 1) // 2


def lastLogTerm(log):
    '''Терм последнего элемента лога'''
    if log:
        return log[-1].term
    else:
        return 0


def otherServers(this):
    '''Список адресов всех серверов, кроме данного'''
    seq = list(range(1, NETWORK_SIZE + 1))
    seq.remove(this)
    return seq


class RaftClient:
    def __init__(self, parent):
        self.parent = parent

    def run(self):
        '''Бесконечный цикл отсчёта времени и инициации выборов, когда приходит время'''
        self.parent.startTime = time.time()
        while True:
            timeDiff = time.time() - self.parent.startTime
            if self.parent.state != LEADER and timeDiff > self.parent.timeout:
                '''У сервера таймаут'''
                logging.info(f"Node {self.parent.selfID} timed out at {timeDiff} s with the limit of "
                             f"{self.parent.timeout} s\n")
                votes = 0
                try:
                    for i in otherServers(self.parent.selfID):
                        '''Рассылаем VoteRequest'''
                        with grpc.insecure_channel(OPEN_ADDRESS.format(i)) as channel:
                            stub = raft_server_pb2_grpc.RaftServerStub(channel)
                            logging.debug(f"Node {self.parent.selfID} created a stub using channel "
                                          f"{OPEN_ADDRESS.format(i)}")
                            response = stub.RequestVote(raft_server_pb2.VoteRequest(
                                term=self.parent.currentTerm, candidateID=self.parent.selfID,
                                lastLogIndex=len(self.parent.log),
                                lastLogTerm=lastLogTerm(self.parent.log)
                            ))
                            votes += response.voteGranted
                            if votes == MAJORITY:
                                self.state = LEADER
                                logging.info(f"Node {self.parent.selfID} became the leader\n")
                                break
                except Exception as e:
                    print(traceback.format_exc())
            time.sleep(HEARTBEAT / 1000)
