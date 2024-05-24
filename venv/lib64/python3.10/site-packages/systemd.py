import warnings

from cysystemd import (
    async_reader, _daemon, daemon, _journal, journal, reader,
    package_info, version_info, author_info, author_email, license,
    __version__, __author__
)

__all__ = (
    "async_reader", "_daemon", "daemon", "_journal", "journal", "reader",
    "__author__", "__version__", "author_info", "license",
    "package_info", "version_info",
)


warnings.warn(
    "This package has been renamed to cysystemd, please use this instead.",
    DeprecationWarning
)
