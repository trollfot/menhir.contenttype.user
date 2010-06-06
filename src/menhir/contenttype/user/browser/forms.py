## -*- coding: utf-8 -*-

import grokcore.view as grok
import dolmen.app.layout as layout

from dolmen import menu
from dolmen.app.authentication.interfaces import IChangePassword
from dolmen.forms.crud import utils
from dolmen.forms.base import Fields
from zeam.form.ztk import action
from menhir.contenttype.user import IUser, MF as _

from zope.formlib.interfaces import IWidgetInputError
from zope.interface import implements
from zope.schema import ValidationError


class DuplicatedLogin(ValidationError):
    implements(IWidgetInputError)
    __doc__ = _(u"This user identifier is already in use.")


class UserAdd(layout.Add):
    grok.name("useradd")
    grok.require('dolmen.security.AddUsers')

    fields = (Fields(IUser).omit('password') + Fields(IChangePassword)).select(
        'id', 'title', 'email', 'portrait', 'password', 'verify_pass')

    def update(self):
        layout.Add.update(self)
        #import pdb
        #pdb.set_trace()


@menu.menuentry(layout.ContextualMenu)
class UserEdit(layout.Edit):
    grok.name('edit')
    grok.context(IUser)
    fields = Fields(IUser).select('title', 'email', 'portrait')


@menu.menuentry(layout.ContextualMenu)
class UserPassword(layout.Edit):
    grok.context(IUser)
    grok.name('change_passwd')
    grok.title(_("Change password"))
    grok.require("dolmen.content.Edit")

    fields = Fields(IChangePassword)
    label = _('Change password')
