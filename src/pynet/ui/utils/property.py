# -*- coding: utf-8 -*-

from PySide6 import QtCore, QtGui, QtQml
from .cache import Cache

PROPERTY_CACHE = Cache('ui-cache.yml')


def signal_attribute_name(property_name):
    """ Return a magic key for the attribute storing the signal name. """
    return f"_property_{property_name}_signal_"


def value_attribute_name(property_name):
    """ Return a magic key for the attribute storing the property value. """
    return f"_property_{property_name}_value_"


class PropertyMeta(type(QtCore.QObject)):
    def __new__(cls, name, bases, attrs):
        for key in list(attrs.keys()):
            attr = attrs[key]
            if not isinstance(attr, Property):
                continue
            initial_value = attr.initial_value
            type_ = type(initial_value)
            notifier = QtCore.Signal(type_)
            save = attr.save
            attrs[key] = PropertyImpl(initial_value, name=key, type_=type_, notify=notifier, save=save)
            attrs[signal_attribute_name(key)] = notifier

        return super().__new__(cls, name, bases, attrs)


class Property:
    """ Property definition.

    This property will be patched by the PropertyMeta metaclass into a PropertyImpl type.
    """

    def __init__(self, initial_value, name="", save=False):
        self.initial_value = initial_value
        self.name = name
        self.save = save

    @staticmethod
    def save_cache():
        PROPERTY_CACHE.save()


class PropertyImpl(QtCore.Property):
    """ Actual property implementation using a signal to notify any change. """

    def __init__(self, initial_value, name="", type_=None, notify=None, save=False):
        super().__init__(type_, self.getter, self.setter, notify=notify)
        self.initial_value = PROPERTY_CACHE.get(name, initial_value)
        self.name = name
        self.save = save

    def getter(self, inst):
        return getattr(inst, value_attribute_name(self.name), self.initial_value)

    def setter(self, inst, value):
        last_value = getattr(inst, self.name)
        if last_value != value:
            setattr(inst, value_attribute_name(self.name), value)
            notifier_signal = getattr(inst, signal_attribute_name(self.name))
            notifier_signal.emit(value)
            if self.save:
                PROPERTY_CACHE.data.update({self.name: value})
