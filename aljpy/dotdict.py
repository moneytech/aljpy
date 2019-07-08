import pandas as pd
import numpy as np
from collections import OrderedDict

def treestr(t):
    """Stringifies a tree structure. These turn up all over the place in my code, so it's worth factoring out"""
    key_length = max(map(len, map(str, t.keys()))) if t.keys() else 0
    max_spaces = 4 + key_length
    val_length = 119 - max_spaces
    
    d = {}
    for k, v in t.items():
        if hasattr(v, 'shape'):                    
            d[k] = f'{tuple(v.shape)}-{type(v).__name__}'
        elif type(v) in (list, set, dict):
            d[k] = f'({len(v)},)-{type(v).__name__}'
        elif type(v) in (type(t),):
            d[k] = str(v)
        else:
            d[k] = f'{str(v).splitlines()[0][:val_length]} ...'

    s = [f'{type(t).__name__}:']
    for k, v in d.items():
        lines = v.splitlines() or ['']
        s.append(str(k) + ' '*(max_spaces - len(str(k))) + lines[0])
        for l in lines[1:]:
            s.append(' '*max_spaces + l)
        # if len(lines) > 1:
        #     s.append('\n')

    return '\n'.join(s)

class dotdict(OrderedDict):
    
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
    def __dir__(self):
        return sorted(set(super().__dir__() + list(self.keys())))

    def __getattr__(self, k):
        if k in self:
            return self[k]
        raise AttributeError(k)
    
    def __str__(self):
        return treestr(self)
    
    def __repr__(self):
        return self.__str__()

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)
    
    def copy(self):
        return dotdict(super().copy()) 
    
    def pipe(self, f, *args, **kwargs):
        return f(self, *args, **kwargs)

