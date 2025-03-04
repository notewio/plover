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

from pywayland.protocol_core import Global, Interface, Proxy, Resource


class WlBuffer(Interface):
    """Content for a :class:`~pywayland.protocol.wayland.WlSurface`

    A buffer provides the content for a
    :class:`~pywayland.protocol.wayland.WlSurface`. Buffers are created through
    factory interfaces such as :class:`~pywayland.protocol.wayland.WlShm`,
    wp_linux_buffer_params (from the linux-dmabuf protocol extension) or
    similar. It has a width and a height and can be attached to a
    :class:`~pywayland.protocol.wayland.WlSurface`, but the mechanism by which
    a client provides and updates the contents is defined by the buffer factory
    interface.

    If the buffer uses a format that has an alpha channel, the alpha channel is
    assumed to be premultiplied in the color channels unless otherwise
    specified.
    """

    name = "wl_buffer"
    version = 1


class WlBufferProxy(Proxy):
    interface = WlBuffer

    @WlBuffer.request()
    def destroy(self):
        """Destroy a buffer

        Destroy a buffer. If and how you need to release the backing storage is
        defined by the buffer factory interface.

        For possible side-effects to a surface, see :func:`WlSurface.attach()
        <pywayland.protocol.wayland.WlSurface.attach>`.
        """
        self._marshal(0)
        self._destroy()


class WlBufferResource(Resource):
    interface = WlBuffer

    @WlBuffer.event()
    def release(self):
        """Compositor releases buffer

        Sent when this :class:`WlBuffer` is no longer used by the compositor.
        The client is now free to reuse or destroy this buffer and its backing
        storage.

        If a client receives a release event before the frame callback
        requested in the same :func:`WlSurface.commit()
        <pywayland.protocol.wayland.WlSurface.commit>` that attaches this
        :class:`WlBuffer` to a surface, then the client is immediately free to
        reuse the buffer and its backing storage, and does not need a second
        buffer for the next surface content update. Typically this is possible,
        when the compositor maintains a copy of the
        :class:`~pywayland.protocol.wayland.WlSurface` contents, e.g. as a GL
        texture. This is an important optimization for GL(ES) compositors with
        :class:`~pywayland.protocol.wayland.WlShm` clients.
        """
        self._post_event(0)


class WlBufferGlobal(Global):
    interface = WlBuffer


WlBuffer._gen_c()
WlBuffer.proxy_class = WlBufferProxy
WlBuffer.resource_class = WlBufferResource
WlBuffer.global_class = WlBufferGlobal
