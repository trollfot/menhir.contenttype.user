# -*- coding: utf-8 -*-

import grok
from menhir.contenttype.user import IUser
from dolmen.app.layout import models as layout


class UserView(layout.Index):
    grok.context(IUser)
    grok.name('index')

    def update(self):
        url = self.url(self.context)
        if self.context.portrait is not None:
            self.thumbnail = "%s/++thumbnail++portrait.thumb" % url
            self.popup_url = "%s/++thumbnail++portrait.large" % url
