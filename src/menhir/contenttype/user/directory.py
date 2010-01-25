# -*- coding: utf-8 -*-

import grok
import dolmen.content
from zope.container.interfaces import INameChooser
from zope.exceptions.interfaces import UserError
from dolmen.app.authentication.plugins import PrincipalFolderPlugin


class Directory(PrincipalFolderPlugin):
    dolmen.content.icon("directory.png")
    dolmen.content.name("User directory")
    dolmen.content.require('dolmen.security.ManageUsers')


class UserNameChooser(grok.Adapter):
    grok.context(Directory)
    grok.implements(INameChooser)

    def checkName(self, name, object):
        # here, raise UserError on some tests.
        return not name in self.context

    def chooseName(self, name, object):
        return object.id
