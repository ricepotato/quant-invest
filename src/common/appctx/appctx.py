
import sys
import importlib

from .exc import *

def handle_invalid_init_args(func):
    def wrapper(*args, **kwargs):
        try:
            return func
        except TypeError as e:
            raise InvalidInitArgs()

    return wrapper

class AppContext(object):
    def __init__(self, ctx):
        self.ctx = ctx

    def get_bean(self, name):
        ctx = self.get_ctx(name)
        args = self.get_init_args(ctx)
        kwargs = self.get_init_kwargs(ctx)
        properties = self.get_properties(ctx)
        cls = self.get_mod_obj(ctx["class"])
        inst = self.create_instance(cls, args, kwargs)
        inst = self.add_properties(inst, properties)
        return inst

    def get_ctx(self, name):
        try:
            return self.ctx[name]
        except KeyError as e:
            raise InvalidBeanName("InvalidBeanName. {}".format(name))

    def get_mod_obj(self, path):
        """ TODO : . 없는 현재폴더 클래스 임포트 필요한지 여부? 구현 """
        try:
            path_list = path.split(".")
            mod = importlib.import_module(".".join(path_list[0:-1]))
            return getattr(mod, path_list[-1])
        except (ImportError, IndexError, AttributeError) as e:
            raise InvalidModulePath("Invalid Module Path. {}".format(path))

    def get_init_args(self, ctx):
        init_args = ctx.get("init_args", [])
        return map(lambda item : self.get_obj(item), init_args)

    def get_init_kwargs(self, ctx):
        return self._extract_arg_dict(ctx, "init_kwargs")

    def get_obj(self, arg):
        if "bean" in arg:
            return self.get_bean(arg["bean"])
        elif "value" in arg:
            return arg["value"]
        else:
            raise InvalidArgObjType("Invalid arg type. {}".format(str(arg)))

    def get_properties(self, ctx):
        return self._extract_arg_dict(ctx, "properties")

    def _extract_arg_dict(self, ctx, name):
        init_obj = ctx.get(name, {})
        res = {}
        for key, val in init_obj.items():
            res[key] = self.get_obj(val)
        return res

    def add_properties(self, inst, properties):
        for key, val in properties.items():
            setattr(inst, key, val)
        return inst

    @handle_invalid_init_args
    def create_instance(self, cls, args, kwargs):
        if args and kwargs:
            return cls(*args, **kwargs)
        elif args:
            return cls(*args)
        elif kwargs:
            return cls(**kwargs)
        else:
            return cls()



            





