##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from zojax.pageelement.interfaces import IPageElement

_ = MessageFactory('zojax.persistentpageelement')


class IPersistentPageElement(IPageElement):
    """ page element """

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Page element title'),
        default = u'',
        missing_value = u'',
        required = False)

    description = schema.Text(
        title = _(u'Description'),
        description = _(u'Page element description'),
        default = u'',
        missing_value = u'',
        required = False)

    def getSource():
        """Get the source of the page element."""

    def setSource(text, content_type='text/html'):
        """Save the source of the page element.

        'text' must be Unicode.
        """

    source = schema.SourceText(
        title=_("Source"),
        description=_("The source of the page element."),
        required=True)


class IPageElementsConfiglet(interface.Interface):
    """ configlet """

    elements = interface.Attribute('Page elements container')
