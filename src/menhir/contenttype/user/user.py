# -*- coding: utf-8 -*-

import grok
import dolmen.content

from zope.interface import Interface
from zope.component import getUtility
from zope.annotation.attribute import AttributeAnnotations
from zope.password.interfaces import IPasswordManager

from dolmen.file import ImageField
from dolmen.blob import BlobProperty
from dolmen.authentication import IPasswordChecker
from dolmen.app.authentication import IUser as IBaseUser
from menhir.contenttype.user import MF as _


class IUser(IBaseUser):
    portrait = ImageField(
        title = _(u"Portrait"),
        required = False,
        default = None
        )


class UserFactory(dolmen.content.Factory):
    grok.name('menhir.user')
    addform = u"useradd"


class User(dolmen.content.Container):
    dolmen.content.icon('user.png')
    dolmen.content.name(_('User'))
    dolmen.content.require('dolmen.security.AddUsers')
    dolmen.content.schema(IUser)
    grok.implements(IPasswordChecker)

    portrait = BlobProperty(IUser['portrait'])

    def __init__(self):
        dolmen.content.Container.__init__(self)
        self._password = u""

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        passwordmanager = getUtility(IPasswordManager, 'SHA1')
        self._password = passwordmanager.encodePassword(password)

    def checkPassword(self, password):
        passwordmanager = getUtility(IPasswordManager, 'SHA1')
        return passwordmanager.checkPassword(self.password, password)


class UserAnnotations(AttributeAnnotations, grok.Adapter):
    """Defines the annotations used on a user. This overrides the
    use of zope.app.principalannotations.
    """
