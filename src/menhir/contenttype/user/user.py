# -*- coding: utf-8 -*-

import grok
import dolmen.content

from zope.interface import Interface
from zope.component import getUtility
from zope.app.authentication.interfaces import IPasswordManager

from dolmen.blob import BlobProperty
from dolmen.imaging import ImageField
from dolmen.app.layout import models as layout
from dolmen.app.authentication import IUser, IPasswordChecker
from menhir.contenttype.user import mf as _


class IPortrait(Interface):
    portrait = ImageField(
        title = _(u"Portrait"),
        required = False,
        default = None
        )


class UserFactory(dolmen.content.Factory):
    grok.name('menhir.user')
    addform = "useradd"


class User(dolmen.content.Container):
    dolmen.content.name('User')
    dolmen.content.icon('user.png')
    dolmen.content.schema(IUser, IPortrait)
    dolmen.content.require('dolmen.security.AddUsers')
    grok.implements(IPasswordChecker)

    relations = None
    portrait = BlobProperty(IPortrait['portrait'])

    def __init__(self):
        dolmen.content.Container.__init__(self)
        self._password = u""
        
    def get_password(self):
        return self._password
        
    def set_password(self, password):
        passwordmanager = getUtility(IPasswordManager, 'SHA1')
        self._password = passwordmanager.encodePassword(password)

    password = property(get_password, set_password)

    def checkPassword(self, password):
        passwordmanager = getUtility(IPasswordManager, 'SHA1')
        return passwordmanager.checkPassword(self.password, password)


class UserView(layout.Index):
    grok.name('index')

    def update(self):
        url = self.url(self.context)
        if self.context.portrait is not None:
            self.thumbnail = "%s/++thumbnail++portrait.thumb" % url
            self.popup_url = "%s/++thumbnail++portrait.large" % url       
