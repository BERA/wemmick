import os
from urllib.parse import urlparse


def file_relative_path(dunderfile, relative_path: str):
    """
    This function is useful when one needs to load a file that is
    relative to the position of the current file. (Such as when
    you encode a configuration file path in source file and want
    in runnable in any current working directory)

    It is meant to be used like the following:
    file_relative_path(__file__, 'path/relative/to/file')

    H/T https://github.com/dagster-io/dagster/blob/8a250e9619a49e8bff8e9aa7435df89c2d2ea039/python_modules/dagster/dagster/utils/__init__.py#L34
    """
    return os.path.join(os.path.dirname(dunderfile), relative_path)


def get_scheme(path: str):
    return urlparse(path).scheme


def check_file_exists(path):
    if not os.path.isfile(path):
        raise ValueError(
            f"File {path} was not found. Please check the path and try again."
        )


def read_local_file(path):
    file_path = urlparse(path).path
    check_file_exists(file_path)

    with open(file_path, "r") as f:
        raw_file = f.read()

    return raw_file


def get_file(path: str):
    scheme = get_scheme(path)
    if scheme == "file":
        return read_local_file(path)
    else:
        raise ValueError(
            f'Invalid scheme "{scheme}", supported schemes are s3, gcp, and file'
        )
