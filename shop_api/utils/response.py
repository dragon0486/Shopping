class BaseResponse(object):

    def __init__(self):
        self.code = 1000
        self.data = None
        self.error = None

    @property
    def dict(self):
        return self.__dict__

class TokenResponse(BaseResponse):
    def __init__(self):
        self.token = None
        super(TokenResponse,self).__init__()
