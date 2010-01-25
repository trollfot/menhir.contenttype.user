# -*- coding: utf-8 -*-

import os.path
import grokcore.component as grok

from dolmen.thumbnailer import IImageMiniaturizer
from dolmen.authentication import IPrincipalFolder

from zope.interface import Interface
from zope.traversing.interfaces import ITraversable
from zope.component import getUtility, getMultiAdapter
from zope.publisher.interfaces.http import IHTTPRequest
from zope.app.publisher.fileresource import Image
from zope.app.publisher.browser.fileresource import FileResource

PATH = os.path.dirname(os.path.abspath(__file__))
BASE_AVATAR = Image(os.path.join(PATH, 'unknown.gif'), 'unknown.gif')


class AvatarRetriever(grok.MultiAdapter):
    grok.name('avatar')
    grok.provides(ITraversable)
    grok.adapts(Interface, IHTTPRequest)

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, userid, ignore):
        users = getUtility(IUserDirectory)
        user = users.getUserByLogin(userid)
        if user is not None and user.portrait is not None:
            thumbs = IImageMiniaturizer(user)
            thumb = thumbs.retrieve('square', fieldname='portrait')
            if thumb is not None:
                return getMultiAdapter((thumb, self.request),
                                       name = "file_publish")
        
        resource = FileResource(BASE_AVATAR, self.request)
        return resource
