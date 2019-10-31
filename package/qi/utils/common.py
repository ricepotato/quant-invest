#-*- coding: utf-8 -*-

import inspect

class Dictionary(dict):
    
    def __getattr__(self, key):
        return self[key]

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Serializer(object):
    obj_map = {}

    def to_dict(self):
        ret = Dictionary()
        self.obj_map[id(self)] = ret
        for key in inspect(self).attrs.keys():
            ret[key] = getattr(self, key)
        return ret

class Singleton(type):
    """Singleton.
    @see: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]