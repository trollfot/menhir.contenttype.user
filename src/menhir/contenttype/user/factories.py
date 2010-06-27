# -*- coding: utf-8 -*-

import grokcore.component as grok

from zope.authentication.interfaces import IAuthentication
from zope.component import getUtility
from zope.event import notify
from zope.location.interfaces import ILocation
from zope.pluggableauth.interfaces import (
    AuthenticatedPrincipalCreated, IAuthenticatedPrincipalFactory)
from zope.publisher.interfaces import IRequest
from zope.security.interfaces import IGroupClosureAwarePrincipal as IPrincipal


class LocatablePrincipal(object):
    grok.implements(IPrincipal, ILocation)

    def __init__(self, info):
        self.id = info.id
        self.title = info.title
        self.description = info.description
        self.groups = ["zope.Authenticated", "zope.Everybody"]
        self.__name__ = info.__name__
        self.__parent__ = info.__parent__

    def __repr__(self):
        return 'LocatablePrincipal(%r)' % self.id

    @property
    def allGroups(self):
        """This needs to be computed somehow.
        """
        if self.groups:
            seen = set()
            principals = getUtility(IAuthentication)
            stack = [iter(self.groups)]
            while stack:
                try:
                    group_id = stack[-1].next()
                except StopIteration:
                    stack.pop()
                else:
                    if group_id not in seen:
                        yield group_id
                        seen.add(group_id)
                        group = principals.getPrincipal(group_id)
                        stack.append(iter(group.groups))


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
