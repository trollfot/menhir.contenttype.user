# -*- coding: utf-8 -*-

import os.path

import grokcore.component as grok

from zope.browserresource.file import File, FileResource
from zope.component import getUtility, getMultiAdapter
from zope.interface import Interface
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.interfaces import ITraversable

from dolmen.app.authentication.interfaces import IUserDirectory
from dolmen.thumbnailer import IImageMiniaturizer

PATH = os.path.dirname(os.path.abspath(__file__))
BASE_AVATAR = File(os.path.join(PATH, 'unknown.gif'), 'unknown.gif')


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
                                       name="file_publish")

        resource = FileResource(BASE_AVATAR, self.request)
        return resource
