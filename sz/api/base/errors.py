class ApiError(Exception):

    def __init__(self, err_msg: str, err_code: int = -1, ):
        self.err_code = err_code
        self.err_msg = err_msg
