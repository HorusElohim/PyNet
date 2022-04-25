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


import os
from pathlib import Path
from pympler import asizeof


class Size:
    # bytes pretty-printing
    UNITS_MAPPING = [
        (1 << 50, ' PB'),
        (1 << 40, ' TB'),
        (1 << 30, ' GB'),
        (1 << 20, ' MB'),
        (1 << 10, ' KB'),
        (1, ' byte'),
    ]

    @staticmethod
    def pretty_size(num_bytes: int) -> str:
        """Get human-readable file sizes.
        simplified version of https://pypi.python.org/pypi/hurry.filesize/

        :param:
            num_bytes : file size

        :return:
            size human-readable

        """
        suffix = ''
        factor = 1
        for factor, suffix in Size.UNITS_MAPPING:
            if num_bytes >= factor:
                break
        amount = int(num_bytes / factor)
        if suffix == 'byte' and amount > 9:
            suffix += 's'

        return str(amount) + suffix

    @staticmethod
    def obj_size(obj: object) -> int:
        """
        Get human-readable Python object size

        :param: obj: Target python object
        :return: size in bytes

        Examples:
            >>> Size.obj_size(int())
            >>> 24

        """
        return int(asizeof.asizeof(obj))

    @staticmethod
    def pretty_obj_size(obj: object) -> str:
        """
        Get human-readable Python object size

        :param: obj: Target python object
        :return: human-readable size

        Examples:
            >>> Size.pretty_obj_size(int())
            >>> '24 byte'

        """
        return Size.pretty_size(asizeof.asizeof(obj))

    @staticmethod
    def folder_size(folder: str) -> int:
        """
        Get folder size in bytes

        :param folder: target folder
        :return: size in bytes

        Examples:
            >>> Size.folder_size('/etc/apt/')
            >>> 55818

        """
        return sum(file.stat().st_size for file in Path(folder).rglob('*'))

    @staticmethod
    def pretty_folder_size(folder: str) -> str:
        """
        Get human-readable Python object size

        :param: folder: target folder
        :return: human-readable size

        Examples:
            >>> Size.pretty_folder_size('/etc/apt/')
            >>> '54 KB'

        """
        return Size.pretty_size(Size.folder_size(folder))

    @staticmethod
    def file_size(file: str) -> int:
        """
        Get File size

        :param: file: target folder
        :return: file size in bytes

        Examples:
            >>> Size.file_size('/etc/apt/sources.list')
            >>> 3159
        """
        return os.path.getsize(file)

    @staticmethod
    def pretty_file_size(file: str) -> str:
        """
        Get human-readable Python object size

        :param: file: target folder
        :return: file human-readable size

        Examples:
            >>> Size.pretty_file_size('/etc/apt/sources.list')
            >>> '3 KB'
        """
        return Size.pretty_size(os.path.getsize(file))
