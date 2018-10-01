from enum import Enum


class ServiceCodes(Enum):
    EMPTY_PARAMS = 'S3001'
    BAD_PARAMS = 'S3002'
    FAIL = 'S3003'


class ServiceException(BaseException):
    def __init__(self, errorcode, msg=None):
        self._errorcode = errorcode
        self._msg = msg

        super(ServiceException, self).__init__('[%s] - %s' % (self.errorcode.value, self.message))

    @property
    def errorcode(self):
        return self._errorcode

    @property
    def message(self):
        return self._msg
