#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from setuptools import setup

setup(
    name = 'trac-NewTicketMacro',
    version = '0.1',
    packages = ['newticketmacro'],
    package_data={ 'newticketmacro' : [ 'templates/*.html', "htdocs/*.*" ] },
    author = "Ethan Jucovy",
    description = "Macro to add a form to a wiki page for creating new tickets",
    license = "BSD",
    keywords = "trac plugin macro wiki",
    classifiers = [
        'Framework :: Trac',
    ],
    
    entry_points = {
        'trac.plugins': [
            'newticketmacro.macro = newticketmacro.macro',
        ],
    },
)
