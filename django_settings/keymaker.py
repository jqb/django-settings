import sys

class KeyMaker(object):
    def __init__(self, prefix):
        self.prefix = prefix

    def convert(self, arg):
        if sys.version_info < (3,) and isinstance(arg, unicode):
            return arg.encode(django.settings.DEFAULT_CHARSET)
        return str(arg)

    def args_to_key(self, args):
        return ":".join(map(self.convert, args))

    def kwargs_to_key(self, kwargs):
        return ":".join([
            "%s:%s" % (self.convert(k), self.convert(v))
            for k, v in kwargs.items()
        ])

    def make(self, method_name, args, kwargs):
        key = ":".join((
            self.prefix,
            method_name,
            self.args_to_key(args),
            self.kwargs_to_key(kwargs),
        ))
        return key


