# -*- coding: utf-8 -*-
# Public module API
from .models import Model, Setting, registry
from .moduleregistry import RegisterError
from .discover import autoregister
from .dataapi import DataAPI, data


# expose methods
register = registry.register
unregister = registry.unregister
unregister_all = registry.unregister_all


# shortcuts
get = data.get
set = data.set
exists = data.exists
type_names = data.type_names

