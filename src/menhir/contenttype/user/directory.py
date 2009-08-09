# -*- coding: utf-8 -*-

import grok
import dolmen.content as content
from dolmen.app.authentication import IUserDirectory
from zope.interface import implements
from zope.app.container.interfaces import INameChooser


class Directory(content.Container):
    implements(IUserDirectory)
    content.icon("directory.png")
    content.name("User directory")
    content.schema(content.IBaseContent)
    content.require('dolmen.security.ManageUsers')

    def getIdByLogin(self, login):
        if login in self.keys():
            return login
        return None

    def getUserByLogin(self, login):
        return self.get(login)


class UserNameChooser(grok.Adapter):
    grok.context(Directory)
    grok.implements(INameChooser)

    def checkName(self, name, object):
        return not name in self.context

    def chooseName(self, name, object):
        return object.id
