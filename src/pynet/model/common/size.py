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
        Args:
            num_bytes : file size
        Return:
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
    def get_obj_size(obj: object) -> str:
        """
        Get human-readable Python object size
        :param obj:
        :return: human-readable size
        """
        return Size.pretty_size(asizeof.asizeof(obj))

    @staticmethod
    def get_folder_size_byte(folder: str) -> int:
        """
        Get human-readable Python object size
        :param folder: target folder
        :return: size in bytes
        """
        return sum(file.stat().st_size for file in Path(folder).rglob('*'))

    @staticmethod
    def get_folder_size(folder: str) -> str:
        """
        Get human-readable Python object size
        :param folder: target folder
        :return: human-readable size
        """
        return Size.pretty_size(Size.get_folder_size_byte(folder))

    @staticmethod
    def get_file_size_byte(file: str) -> int:
        """
        Get human-readable Python object size
        :param file: target folder
        :return: file size in bytes
        """
        return os.path.getsize(file)
