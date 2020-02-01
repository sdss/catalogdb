# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.


class CatalogdbError(Exception):
    """A custom core Catalogdb exception"""

    def __init__(self, message=None):

        message = 'There has been an error' \
            if not message else message

        super(CatalogdbError, self).__init__(message)


class CatalogdbNotImplemented(CatalogdbError):
    """A custom exception for not yet implemented features."""

    def __init__(self, message=None):

        message = 'This feature is not implemented yet.' \
            if not message else message

        super(CatalogdbNotImplemented, self).__init__(message)


class CatalogdbMissingDependency(CatalogdbError):
    """A custom exception for missing dependencies."""
    pass


class CatalogdbWarning(Warning):
    """Base warning for Catalogdb."""


class CatalogdbUserWarning(UserWarning, CatalogdbWarning):
    """The primary warning class."""
    pass


class CatalogdbDeprecationWarning(CatalogdbUserWarning):
    """A warning for deprecated features."""
    pass
