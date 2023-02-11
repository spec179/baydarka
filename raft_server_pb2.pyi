from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Heartbeat(_message.Message):
    __slots__ = ["candidateID"]
    CANDIDATEID_FIELD_NUMBER: _ClassVar[int]
    candidateID: int
    def __init__(self, candidateID: _Optional[int] = ...) -> None: ...

class VoteReply(_message.Message):
    __slots__ = ["term", "voteGranted"]
    TERM_FIELD_NUMBER: _ClassVar[int]
    VOTEGRANTED_FIELD_NUMBER: _ClassVar[int]
    term: int
    voteGranted: bool
    def __init__(self, term: _Optional[int] = ..., voteGranted: bool = ...) -> None: ...

class VoteRequest(_message.Message):
    __slots__ = ["candidateID", "lastLogIndex", "lastLogTerm", "term"]
    CANDIDATEID_FIELD_NUMBER: _ClassVar[int]
    LASTLOGINDEX_FIELD_NUMBER: _ClassVar[int]
    LASTLOGTERM_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    candidateID: int
    lastLogIndex: int
    lastLogTerm: int
    term: int
    def __init__(self, term: _Optional[int] = ..., candidateID: _Optional[int] = ..., lastLogIndex: _Optional[int] = ..., lastLogTerm: _Optional[int] = ...) -> None: ...
