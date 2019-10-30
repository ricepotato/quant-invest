
class AppContextError(Exception):
    pass

class InvalidBeanName(AppContextError):
    pass

class InvalidArgObjType(AppContextError):
    pass

class InvalidModulePath(AppContextError):
    pass

class InvalidInitArgs(AppContextError):
    pass