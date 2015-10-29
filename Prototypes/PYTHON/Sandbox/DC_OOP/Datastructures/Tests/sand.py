__author__ = 'benjamin'

class base(object):
    
    def __init__(self):
        self._foo = 1

class derived(base):
    
    def __init__(self):
        base.__init__(self)
        self._bar = 2

    def print_foo(self):
        print self._foo

a = derived()
a.print_foo()