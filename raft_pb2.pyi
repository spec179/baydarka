from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VoteReply(_message.Message):
    __slots__ = ["return_term", "voteGranted"]
    RETURN_TERM_FIELD_NUMBER: _ClassVar[int]
    VOTEGRANTED_FIELD_NUMBER: _ClassVar[int]
    return_term: int
    voteGranted: bool
    def __init__(self, return_term: _Optional[int] = ..., voteGranted: bool = ...) -> None: ...

class VoteRequest(_message.Message):
    __slots__ = ["id", "term"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TERM_FIELD_NUMBER: _ClassVar[int]
    id: int
    term: int
    def __init__(self, id: _Optional[int] = ..., term: _Optional[int] = ...) -> None: ...
