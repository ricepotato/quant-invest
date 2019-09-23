class Dictionary(dict):
    
    def __getattr__(self, key):
        return self[key]

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
