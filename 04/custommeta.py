# pylint: disable=missing-docstring

class CustomMeta(type):

    _prefix = 'custom_'

    def __setattr__(cls, name, val):
        if hasattr(cls, name):
            super().__setattr__(name, val)
            return
        super().__setattr__(CustomMeta._prefix+name, val)

    @staticmethod
    def _custom_setattr(obj, name, value):
        if hasattr(obj, name):
            obj.__dict__[name] = value
            return
        obj.__dict__[CustomMeta._prefix+name] = value

    def __new__(mcs, name, bases, classdict):
        for key in classdict.copy().keys():
            if key.startswith('__') and key.endswith('__'):
                continue
            classdict[mcs._prefix+key] = classdict.pop(key)
        classdict['__setattr__'] = mcs._custom_setattr
        cls = super().__new__(mcs, name, bases, classdict)
        return cls
