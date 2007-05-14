# PyGEP: Gene Expression Programming for Python
# Copyright (C) 2007  Ryan J. O'Neil
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import functools


def cache(func):
    '''
    Decorator for caching the return value of an instance level method in self.
    Assumes that there are no arguments passed to the method (not memoization).
    The return value is cached on self._{method}_cache where {method} is the
    name of the method.
    
        @cache
        def _get_something(self):
            ...
            return 'something'
    '''
    cache_name = '_%s_cache' % func.func_name

    @functools.wraps(func)
    def wrapper(self):
        try:
            return getattr(self, cache_name)
            
        except AttributeError:
            setattr(self, cache_name, func(self))
            return getattr(self, cache_name)

    return wrapper


def memoize(func):
    '''
    Decorator for memoizing a function based on its arguments.  Results are
    stored in self._{method}_memo where {method} is the name of the method.
    Note that the args must be hashable, thus lists can't be memoized.
    
        @memoize
        def _compute_something(self, arg1, arg2):
            ...
            return 'something'
    '''
    memo_name = '_%s_memo' % func.func_name
    
    @functools.wraps(func)
    def wrapper(self, *args):
        try:
            memo = getattr(self, memo_name)
        except AttributeError:
            # Haven't memoized anything yet
            memo = {}
            setattr(self, memo_name, memo)
        
        try:
            return memo[args]
        except KeyError:
            # Haven't seen these args yet
            memo[args] = results = func(self, *args)
            return results
    
    return wrapper
