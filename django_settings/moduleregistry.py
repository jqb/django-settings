# -*- coding: utf-8 -*-
"""
moduleregistry
--------------

allows to extend given module by simply registeing classes using "register" method.

Usage::

   >>> import moduleregistry
   >>>
   >>> import mymodule
   >>> import othermodule
   >>>
   >>> assert not hasattr(mymodule, 'OtherClass')  # True
   >>>
   >>> registry = moduleregistry.new_registry(mymodule)
   >>> registry.register(othermodule.OtherClass)
   >>>
   >>> assert hasattr(mymodule, 'OtherClass')  # True, BUT! - it's not the same class
   >>> assert mymodule.OtherClass != othermodule.OtherClass  # True!
   >>> # Subclassing takes place on register invokation
   >>>
   >>> registry.names() == ['OtherClass']  # True
   >>> 'OtherClass' in registry            # True
   >>> registry['OtherClass']              # returns the class
   >>>
   >>>
   >>> registry.register(othermodule.OtherClass)
   >>> # This will raise moduleregistry.RegisterError
   >>>
"""
# system
import sys
import types


def subclass(class_=None, module=None):
    attrs = {
        '__module__': module.__name__,
    }
    return type(class_.__name__, (class_, ), attrs)


class RegisterError(Exception):
    pass


class ModuleRegistry(object):
    def __init__(self, module):
        self.elements = {}
        self.module = module

    def _subclass(self, model_class):
        return subclass(model_class, self.module)

    def register(self, thing, subclass=True):
        name = thing.__name__

        if name in self.elements:
            raise RegisterError('"%s" model already registered on "%s"' % (
                name, self.module.__name__
            ))

        new = thing if not subclass else self._subclass(thing)

        self.elements[name] = new
        setattr(self.module, name, new)

    def unregister(self, name):
        del self.elements[name]
        delattr(self.module, name)

    def unregister_all(self):
        for name in self.elements.keys():
            self.unregister(name)

    def __str__(self):
        return "<%s object %s>" % (self.__class__.__name__, self.elements)

    def __unicode__(self):
        return unicode(str(self))

    def __repr__(self):
        return unicode(self)

    def __contains__(self, model_class_name):
        return model_class_name in self.elements

    def __item__(self):
        return self.elements.values()

    def __getitem__(self, name):
        return self.elements[name]

    def __call__(self, model_class):
        return self.register(model_class)

    def names(self):
        return self.elements.keys()

    def values(self):
        return self.elements.values()


def new_registry(module_or_name):
    if issubclass(module_or_name.__class__, types.ModuleType):
        module = module_or_name
    else:
        module = sys.modules[module_or_name]
    return ModuleRegistry(module)
