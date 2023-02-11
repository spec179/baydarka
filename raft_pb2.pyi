from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Candidate(_message.Message):
    __slots__ = ["candidateId", "lastLogId", "lastLogTerm", "term"]
    CANDIDATEID_FIELD_NUMBER: _ClassVar[int]
    LASTLOGID_FIELD_NUMBER: _ClassVar[int]
    LASTLOGTERM_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    candidateId: int
    lastLogId: int
    lastLogTerm: int
    term: int
    def __init__(self, term: _Optional[int] = ..., candidateId: _Optional[int] = ..., lastLogId: _Optional[int] = ..., lastLogTerm: _Optional[int] = ...) -> None: ...

class Vote(_message.Message):
    __slots__ = ["term", "voteGranted"]
    TERM_FIELD_NUMBER: _ClassVar[int]
    VOTEGRANTED_FIELD_NUMBER: _ClassVar[int]
    term: int
    voteGranted: bool
    def __init__(self, term: _Optional[int] = ..., voteGranted: bool = ...) -> None: ...
