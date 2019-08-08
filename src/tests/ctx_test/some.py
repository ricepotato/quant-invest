
class SomeObj(object):
    
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

class SomeObjWithArg(object):

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

class SomeObjWithArgsKwargs(object):

    def __init__(self, arg1, **kwargs):
        self.arg1 = arg1
        self.kwargs = kwargs