class Module(object):
    def __init__(self, **kargs):
        old_run = self.run.im_func

        def run(self, **kwargs):
            kargs_local = kargs.copy()
            kargs.update(kwargs)
            return old_run(self, **kargs)
        self.run = run.__get__(self, Module)

    def run(self, **kargs):
        print(kargs)


m1 = Module(foo=3, bar='baz')
m1.run()
print(type(m1.run))

m2 = Module(foo=4, qux='bazooka')
m2.run()
print(type(m2.run))
