import jsonpickle
from flask import Response


class ReplyBase(object):

    def __init__(self, ret: int = 0, err_msg: str = 'OK'):
        self.ret = ret
        self.err_msg = err_msg

    def json_str(self) -> str:
        return jsonpickle.encode(self, unpicklable = False, use_decimal = True)


def json_response(reply: ReplyBase) -> Response:
    return Response(jsonpickle.encode(reply, unpicklable = False, use_decimal = True),
                    content_type = 'application/json; charset=utf-8')
