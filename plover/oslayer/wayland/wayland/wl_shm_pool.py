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

from pywayland.protocol_core import Argument, ArgumentType, Global, Interface, Proxy, Resource
from .wl_buffer import WlBuffer


class WlShmPool(Interface):
    """A shared memory pool

    The :class:`WlShmPool` object encapsulates a piece of memory shared between
    the compositor and client.  Through the :class:`WlShmPool` object, the
    client can allocate shared memory
    :class:`~pywayland.protocol.wayland.WlBuffer` objects. All objects created
    through the same pool share the same underlying mapped memory. Reusing the
    mapped memory avoids the setup/teardown overhead and is useful when
    interactively resizing a surface or for many small buffers.
    """

    name = "wl_shm_pool"
    version = 1


class WlShmPoolProxy(Proxy):
    interface = WlShmPool

    @WlShmPool.request(
        Argument(ArgumentType.NewId, interface=WlBuffer),
        Argument(ArgumentType.Int),
        Argument(ArgumentType.Int),
        Argument(ArgumentType.Int),
        Argument(ArgumentType.Int),
        Argument(ArgumentType.Uint),
    )
    def create_buffer(self, offset, width, height, stride, format):
        """Create a buffer from the pool

        Create a :class:`~pywayland.protocol.wayland.WlBuffer` object from the
        pool.

        The buffer is created offset bytes into the pool and has width and
        height as specified.  The stride argument specifies the number of bytes
        from the beginning of one row to the beginning of the next.  The format
        is the pixel format of the buffer and must be one of those advertised
        through the :func:`WlShm.format()
        <pywayland.protocol.wayland.WlShm.format>` event.

        A buffer will keep a reference to the pool it was created from so it is
        valid to destroy the pool immediately after creating a buffer from it.

        :param offset:
            buffer byte offset within the pool
        :type offset:
            `ArgumentType.Int`
        :param width:
            buffer width, in pixels
        :type width:
            `ArgumentType.Int`
        :param height:
            buffer height, in pixels
        :type height:
            `ArgumentType.Int`
        :param stride:
            number of bytes from the beginning of one row to the beginning of
            the next row
        :type stride:
            `ArgumentType.Int`
        :param format:
            buffer pixel format
        :type format:
            `ArgumentType.Uint`
        :returns:
            :class:`~pywayland.protocol.wayland.WlBuffer` -- buffer to create
        """
        id = self._marshal_constructor(0, WlBuffer, offset, width, height, stride, format)
        return id

    @WlShmPool.request()
    def destroy(self):
        """Destroy the pool

        Destroy the shared memory pool.

        The mmapped memory will be released when all buffers that have been
        created from this pool are gone.
        """
        self._marshal(1)
        self._destroy()

    @WlShmPool.request(
        Argument(ArgumentType.Int),
    )
    def resize(self, size):
        """Change the size of the pool mapping

        This request will cause the server to remap the backing memory for the
        pool from the file descriptor passed when the pool was created, but
        using the new size.  This request can only be used to make the pool
        bigger.

        This request only changes the amount of bytes that are mmapped by the
        server and does not touch the file corresponding to the file descriptor
        passed at creation time. It is the client's responsibility to ensure
        that the file is at least as big as the new pool size.

        :param size:
            new size of the pool, in bytes
        :type size:
            `ArgumentType.Int`
        """
        self._marshal(2, size)


class WlShmPoolResource(Resource):
    interface = WlShmPool


class WlShmPoolGlobal(Global):
    interface = WlShmPool


WlShmPool._gen_c()
WlShmPool.proxy_class = WlShmPoolProxy
WlShmPool.resource_class = WlShmPoolResource
WlShmPool.global_class = WlShmPoolGlobal
