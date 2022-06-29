Common
===============================
This is the common section.

.. module:: pynet.model.common

Singleton
_______________________________
.. autoclass:: Singleton
    :members:
    :undoc-members:


Logger
_______________________________

.. autoexception:: LoggerCannotWorkIfBothConsoleAndFileAreDisabled

.. autoenum:: LoggerLevel

.. autoclass:: Logger
    :exclude-members: __weakref__
    :member-order: bysource
    :private-members:
    :inherited-members:
    :members:
    :undoc-members:

Size
_______________________________

.. autoclass:: Size
    :exclude-members: __weakref__
    :member-order: bysource
    :inherited-members:
    :members:
    :undoc-members:

Profiler Decorator
_______________________________

.. autofunction:: profile


Time Helpers
_______________________________

.. autofunction:: pynet.model.common.time.today

.. autofunction:: pynet.model.common.time.now

.. autofunction:: pynet.model.common.time.now_lite
