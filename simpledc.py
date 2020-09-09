# -*- coding: utf-8 -*-
#
# This file is part of dcxml.
# Copyright (C) 2016-2018 CERN.
#
# dcxml is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Generation of Simple Dublin Core XML v1.1.
By default the package will wrap elements in an OAI DC element. This behavior
can be changed by specifying ``container``, ``nsmap`` and ``attribs`` to the
API functions.
"""

# import pkg_resources
from lxml import etree

#  from .jsonutils import validator_factory
from xmlutils import Rules, dump_etree_helper, etree_to_string

rules = Rules()

ns = {
    'dc': 'http://purl.org/dc/elements/1.1/',
    'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
    'xml': 'xml',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
}
"""Default namespace mapping."""

container_attribs = {
    '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation':
    'http://www.openarchives.org/OAI/2.0/oai_dc/ '
    'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
}
"""Default container element attributes."""

container_element = '{http://www.openarchives.org/OAI/2.0/oai_dc/}dc'
"""Default container element."""

def dump_etree(data, container=None, nsmap=None, attribs=None):
    """Convert dictionary to Simple Dublin Core XML as ElementTree.
    :param data: Dictionary.
    :param container: Name (include namespace) of container element.
    :param nsmap: Namespace mapping for lxml.
    :param attribs: Default attributes for container element.
    :returns: LXML ElementTree.
    """
    container = container or container_element
    nsmap = nsmap or ns
    attribs = attribs or container_attribs
    return dump_etree_helper(container, data, rules, nsmap, attribs)


def tostring(data, **kwargs):
    """Convert dictionary to Simple Dublin Core XML as string.
    :param data: Dictionary.
    :param container: Name (include namespace) of container element.
    :param nsmap: Namespace mapping for lxml.
    :param attribs: Default attributes for container element.
    :returns: LXML ElementTree.
    """
    return etree_to_string(dump_etree(data), **kwargs)


def rule_factory(plural, singular):
    """Element rule factory."""
    @rules.rule(plural)
    def f(path, values):
        for v in values:
            if v:
                elem = etree.Element(
                    '{{http://purl.org/dc/elements/1.1/}}{0}'.format(singular))
                elem.text = v
                yield elem
    f.__name__ = plural
    return f


contributors = rule_factory('contributors', 'contributors')

coverage = rule_factory('coverage', 'coverage')

creators = rule_factory('creators', 'creators')

date = rule_factory('date', 'date')

description = rule_factory('description', 'description')

format = rule_factory('format', 'format')

identifier = rule_factory('identifier', 'identifier')

language = rule_factory('languages', 'language')

publisher = rule_factory('publisher', 'publisher')

relation = rule_factory('relation', 'relation')

rights = rule_factory('rights', 'rights')

source = rule_factory('source', 'source')

subject = rule_factory('subject', 'subject')

title = rule_factory('title', 'title')

type = rule_factory('type', 'type')
