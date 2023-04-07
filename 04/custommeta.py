class CustomMeta(type):

    _prefix = 'custom_'

    def __setattr__(self, name, val):
        if hasattr(self, name):
            super().__setattr__(name, val)
            return
        super().__setattr__(CustomMeta._prefix+name, val)

    @staticmethod
    def _custom_setattr(self, name, value):
        if hasattr(self, name):
            self.__dict__[name] = value
            return
        self.__dict__[CustomMeta._prefix+name] = value

    def __new__(mcs, name, bases, classdict, **kwargs):
        for key in classdict.copy().keys():
            if key.startswith('__') and key.endswith('__'):
                continue
            classdict[mcs._prefix+key] = classdict.pop(key)
        classdict['__setattr__'] = mcs._custom_setattr
        cls = super().__new__(mcs, name, bases, classdict)
        return cls
