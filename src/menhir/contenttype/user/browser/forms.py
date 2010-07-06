# -*- coding: utf-8 -*-

import grokcore.view as grok
import dolmen.app.layout as layout

from dolmen import menu
from dolmen.app.authentication.interfaces import IChangePassword
from dolmen.forms.base import Fields
from dolmen.forms.crud import utils
from menhir.contenttype.user import IUser, MF as _
from zeam.form.ztk import action
from zeam.form.base.markers import DISPLAY
from zope.interface import implements
from zope.schema import ValidationError


class UserAdd(layout.Add):
    grok.name("useradd")
    grok.require('dolmen.security.AddUsers')

    fields = (Fields(IUser).omit('password') + Fields(IChangePassword)
              ).select('id', 'title', 'email','portrait', 'password',
                       'verify_pass')


@menu.menuentry(layout.ContextualMenu, order=20)
class UserEdit(layout.Edit):
    grok.name('edit')
    grok.context(IUser)

    fields = Fields(IUser).select('id', 'title', 'email', 'portrait')
    fields['id'].mode = DISPLAY # Will not be extracted, just displayed.


@menu.menuentry(layout.ContextualMenu, order=25)
class UserPassword(layout.Edit):
    grok.context(IUser)
    grok.name('change_passwd')
    grok.title(_("Change password"))
    grok.require("dolmen.content.Edit")

    fields = Fields(IChangePassword)
    label = _('Change password')
