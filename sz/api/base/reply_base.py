import jsonpickle
from flask import Response


class ReplyBase(object):

    def __init__(self, ret: int = 0, err: str = 'OK'):
        self.ret = ret
        self.err = err

    def json_str(self) -> str:
        return jsonpickle.encode(self, unpicklable=False)


def json_response(reply: ReplyBase) -> Response:
    return Response(jsonpickle.encode(reply, unpicklable=False), mimetype='application/json; charset=utf-8')
