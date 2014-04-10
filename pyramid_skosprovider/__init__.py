# -*- coding: utf8 -*-

from zope.interface import Interface

from skosprovider.registry import Registry

from pyramid_skosprovider.utils import (
    json_renderer
)


class ISkosRegistry(Interface):
    pass


def _build_skos_registry(registry):
    skos_registry = registry.queryUtility(ISkosRegistry)
    if skos_registry is not None:
        return skos_registry

    skos_registry = Registry()

    registry.registerUtility(skos_registry, ISkosRegistry)
    return registry.queryUtility(ISkosRegistry)


def get_skos_registry(registry):
    #Argument might be a config or request
    regis = getattr(registry, 'registry', None)
    if regis is None:
        regis = registry
    return regis.queryUtility(ISkosRegistry)


def includeme(config):
    _build_skos_registry(config.registry)

    config.add_renderer('skosjson', json_renderer)

    config.add_directive('get_skos_registry', get_skos_registry)
    config.add_request_method(get_skos_registry, 'skos_registry', reify=True)
    config.add_route(
        'skosprovider.conceptschemes',
        '/conceptschemes'
    )
    config.add_route(
        'skosprovider.conceptscheme',
        '/conceptschemes/{scheme_id}'
    )
    config.add_route(
        'skosprovider.conceptscheme.cs',
        '/conceptschemes/{scheme_id}/c'
    )
    config.add_route(
        'skosprovider.c',
        '/conceptschemes/{scheme_id}/c/{c_id}'
    )

    config.scan()
