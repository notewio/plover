# This file has been autogenerated by the pywayland scanner

# Copyright © 2008-2011 Kristian Høgsberg
# Copyright © 2010-2011 Intel Corporation
# Copyright © 2012-2013 Collabora, Ltd.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice (including the
# next paragraph) shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import enum

from pywayland.protocol_core import Argument, ArgumentType, Global, Interface, Proxy, Resource
from .wl_subsurface import WlSubsurface
from .wl_surface import WlSurface


class WlSubcompositor(Interface):
    """Sub-surface compositing

    The global interface exposing sub-surface compositing capabilities. A
    :class:`~pywayland.protocol.wayland.WlSurface`, that has sub-surfaces
    associated, is called the parent surface. Sub-surfaces can be arbitrarily
    nested and create a tree of sub-surfaces.

    The root surface in a tree of sub-surfaces is the main surface. The main
    surface cannot be a sub-surface, because sub-surfaces must always have a
    parent.

    A main surface with its sub-surfaces forms a (compound) window. For window
    management purposes, this set of
    :class:`~pywayland.protocol.wayland.WlSurface` objects is to be considered
    as a single window, and it should also behave as such.

    The aim of sub-surfaces is to offload some of the compositing work within a
    window from clients to the compositor. A prime example is a video player
    with decorations and video in separate
    :class:`~pywayland.protocol.wayland.WlSurface` objects. This should allow
    the compositor to pass YUV video buffer processing to dedicated overlay
    hardware when possible.
    """

    name = "wl_subcompositor"
    version = 1

    class error(enum.IntEnum):
        bad_surface = 0


class WlSubcompositorProxy(Proxy):
    interface = WlSubcompositor

    @WlSubcompositor.request()
    def destroy(self):
        """Unbind from the subcompositor interface

        Informs the server that the client will not be using this protocol
        object anymore. This does not affect any other objects,
        :class:`~pywayland.protocol.wayland.WlSubsurface` objects included.
        """
        self._marshal(0)
        self._destroy()

    @WlSubcompositor.request(
        Argument(ArgumentType.NewId, interface=WlSubsurface),
        Argument(ArgumentType.Object, interface=WlSurface),
        Argument(ArgumentType.Object, interface=WlSurface),
    )
    def get_subsurface(self, surface, parent):
        """Give a surface the role sub-surface

        Create a sub-surface interface for the given surface, and associate it
        with the given parent surface. This turns a plain
        :class:`~pywayland.protocol.wayland.WlSurface` into a sub-surface.

        The to-be sub-surface must not already have another role, and it must
        not have an existing :class:`~pywayland.protocol.wayland.WlSubsurface`
        object. Otherwise a protocol error is raised.

        Adding sub-surfaces to a parent is a double-buffered operation on the
        parent (see :func:`WlSurface.commit()
        <pywayland.protocol.wayland.WlSurface.commit>`). The effect of adding a
        sub-surface becomes visible on the next time the state of the parent
        surface is applied.

        This request modifies the behaviour of :func:`WlSurface.commit()
        <pywayland.protocol.wayland.WlSurface.commit>` request on the sub-
        surface, see the documentation on
        :class:`~pywayland.protocol.wayland.WlSubsurface` interface.

        :param surface:
            the surface to be turned into a sub-surface
        :type surface:
            :class:`~pywayland.protocol.wayland.WlSurface`
        :param parent:
            the parent surface
        :type parent:
            :class:`~pywayland.protocol.wayland.WlSurface`
        :returns:
            :class:`~pywayland.protocol.wayland.WlSubsurface` -- the new sub-
            surface object ID
        """
        id = self._marshal_constructor(1, WlSubsurface, surface, parent)
        return id


class WlSubcompositorResource(Resource):
    interface = WlSubcompositor


class WlSubcompositorGlobal(Global):
    interface = WlSubcompositor


WlSubcompositor._gen_c()
WlSubcompositor.proxy_class = WlSubcompositorProxy
WlSubcompositor.resource_class = WlSubcompositorResource
WlSubcompositor.global_class = WlSubcompositorGlobal
