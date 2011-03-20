# -*- coding: utf-8 -*-

import grokcore.component as grok

from zope.event import notify
from zope.location.interfaces import ILocation
from zope.pluggableauth.interfaces import (
    AuthenticatedPrincipalCreated, IAuthenticatedPrincipalFactory)
from zope.pluggableauth.factories import Principal
from zope.publisher.interfaces import IRequest
from zope.security.interfaces import IGroupClosureAwarePrincipal as IPrincipal


class ILocatablePrincipal(IPrincipal, ILocation):
    pass


class LocatablePrincipal(Principal):
    grok.implements(ILocatablePrincipal)

    def __init__(self, info):
        self.id = info.id
        self.title = info.title
        self.description = info.description
        self.groups = []
        self.__name__ = info.__name__
        self.__parent__ = info.__parent__

    def __repr__(self):
        return 'LocatablePrincipal(%r)' % self.id


class AuthenticatedPrincipalFactory(grok.MultiAdapter):
    grok.adapts(ILocation, IRequest)
    grok.implements(IAuthenticatedPrincipalFactory)

    def __init__(self, info, request):
        self.info = info
        self.request = request

    def __call__(self, authentication):
        principal = LocatablePrincipal(self.info)
        notify(AuthenticatedPrincipalCreated(
            authentication, principal, self.info, self.request))
        return principal
