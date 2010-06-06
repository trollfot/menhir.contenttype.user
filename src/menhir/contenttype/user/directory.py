# -*- coding: utf-8 -*-

import grokcore.component as grok

from zope.container.interfaces import INameChooser
from zope.pluggableauth.interfaces import IAuthenticatorPlugin

from dolmen.app.authentication.plugins import PrincipalFolderPlugin
import dolmen.content


class IDirectory(IAuthenticatorPlugin):
    """Marker interface.
    """


class Directory(PrincipalFolderPlugin):
    #dolmen.content.icon("directory.png")
    dolmen.content.name("User directory")
    dolmen.content.require('dolmen.security.ManageUsers')
    grok.implements(IDirectory)


class UserNameChooser(grok.Adapter):
    grok.context(Directory)
    grok.implements(INameChooser)

    def checkName(self, name, object):
        # here, raise UserError on some tests.
        return not name in self.context

    def chooseName(self, name, object):
        return object.id
