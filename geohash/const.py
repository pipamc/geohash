# coding: utf-8

# system packages
import sys

# third-party packages

# own packages


class _const(object):

    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const. {}".format(name))
        if not name.isupper():
            raise self.ConstCaseError(
                "const name {} is not all upperrcase".format(name))
        self.__dict__[name] = value

sys.modules["const"] = _const()
