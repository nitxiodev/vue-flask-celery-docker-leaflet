from abc import ABCMeta, abstractmethod


class BaseService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def solve(self, *args):
        raise NotImplementedError('Not implemented yet!')
