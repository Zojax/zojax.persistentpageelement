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
from persistent import Persistent

from zope import interface, component
from zope.app.pagetemplate.engine import TrustedAppPT
from zope.pagetemplate.pagetemplate import PageTemplate
from zope.app.container.contained import Contained
from zope.app.container.interfaces import IObjectMovedEvent
from zojax.content.type.item import PersistentItem

from interfaces import IPersistentPageElement


class PageElement(TrustedAppPT, PageTemplate, PersistentItem):
    interface.implements(IPersistentPageElement)

    expand = False
    errors = ()
    elements = ()

    def getSource(self, request=None):
        return self._text

    def setSource(self, text, content_type='text/html'):
        if not isinstance(text, unicode):
            raise TypeError("source text must be Unicode" , text)
        self.pt_edit(text, content_type)

        if self._v_errors:
            self.errors = self._v_errors
        else:
            self.errors = ()

    source = property(getSource, setSource, None,
                      """Source of the Page Element.""")

    def update(self):
        pass

    def render(self):
        return self.pt_render(self.pt_getContext())

    def updateAndRender(self):
        return self.pt_render(self.pt_getContext())

    def pt_getContext(self):
        namespace = super(PageElement, self).pt_getContext()
        namespace['view'] = self.view
        namespace['request'] = self.request
        namespace['context'] = self.context
        namespace['template'] = self
        return namespace

    def isAvailable(self):
        return True

    def loadElements(self):
        pass

    def __call__(self, context, request, view):
        self._p_activate()

        clone = self.__class__.__new__(self.__class__)
        clone.__dict__.update(self.__dict__)
        clone.__parent__ = view
        clone.context = context
        clone.request = request
        clone.view = view
        return clone


@component.adapter(IPersistentPageElement, IObjectMovedEvent)
def pageElementMoved(element, event):
    sm = component.getSiteManager()

    if event.oldName is not None:
        sm.unregisterAdapter(
            element,
            (interface.Interface, interface.Interface, interface.Interface),
            IPersistentPageElement, event.oldName)

    if event.newName is not None:
        sm.registerAdapter(
            element,
            (interface.Interface, interface.Interface, interface.Interface),
            IPersistentPageElement, event.newName)
