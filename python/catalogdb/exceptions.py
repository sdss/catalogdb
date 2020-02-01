# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-12-05 12:01:21
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-12-05 12:19:32

from __future__ import print_function, division, absolute_import


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


class CatalogdbAPIError(CatalogdbError):
    """A custom exception for API errors"""

    def __init__(self, message=None):
        if not message:
            message = 'Error with Http Response from Catalogdb API'
        else:
            message = 'Http response error from Catalogdb API. {0}'.format(message)

        super(CatalogdbAPIError, self).__init__(message)


class CatalogdbApiAuthError(CatalogdbAPIError):
    """A custom exception for API authentication errors"""
    pass


class CatalogdbMissingDependency(CatalogdbError):
    """A custom exception for missing dependencies."""
    pass


class CatalogdbWarning(Warning):
    """Base warning for Catalogdb."""


class CatalogdbUserWarning(UserWarning, CatalogdbWarning):
    """The primary warning class."""
    pass


class CatalogdbSkippedTestWarning(CatalogdbUserWarning):
    """A warning for when a test is skipped."""
    pass


class CatalogdbDeprecationWarning(CatalogdbUserWarning):
    """A warning for deprecated features."""
    pass
