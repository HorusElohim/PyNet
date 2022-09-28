class DDict(dict):
    """
    a dictionary that supports dot notation
    as well as dictionary access notation
    usage: d = Param() or d = Param({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct=None, **kwargs) -> None:
        if dct:
            data_in = {**dct, **kwargs}
        else:
            data_in = kwargs
        for key, value in data_in.items():
            if hasattr(value, 'keys'):
                value = DDict(value)
            self[key] = value

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)
        self.__dict__ = self
