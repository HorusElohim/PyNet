# Copyright (C) 2022 HorusElohim
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


from zmq import Context
from typing import List, Any, Union
from ..core import BaseChannel, Connection
from . import BasePattern, MethodNotSupported


class Publisher(BasePattern):
    def __init__(self, name: str, channel: BaseChannel, context: Context):
        super().__init__(name, Connection.Type.publisher)
        self.add(channel, context)
        self.log.debug('Constructed')

    def receive(self) -> Union[Any, List[Any]]:
        raise MethodNotSupported(self, 'receive')
